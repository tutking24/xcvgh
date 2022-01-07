from datetime import datetime

import os

from IGitt.GitLab import GitLabOAuthToken, GitLabPrivateToken
from IGitt.GitLab.GitLabContent import GitLabContent
from IGitt.GitLab.GitLabMergeRequest import GitLabMergeRequest
from IGitt.GitLab.GitLabRepository import GitLabRepository
from IGitt.GitLab.GitLabUser import GitLabUser
from IGitt.Interfaces import AccessLevel
from IGitt.Interfaces import IssueStates
from IGitt.Interfaces import MergeRequestStates
from IGitt.Interfaces.Repository import WebhookEvents
from IGitt import ElementAlreadyExistsError, ElementDoesntExistError

from tests import IGittTestCase


class GitLabRepositoryTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.repo = GitLabRepository(self.token,
                                     'gitmate-test-user/test')

        self.fork_token = GitLabPrivateToken(os.environ.get('GITLAB_TEST_TOKEN_2', ''))
        self.fork_repo = GitLabRepository(self.fork_token,
                                          'gitmate-test-user/test')

    def test_id(self):
        self.assertEqual(self.repo.identifier, 3439658)

    def test_id_init(self):
        repo = GitLabRepository(self.token, 3439658)
        self.assertEqual(repo.full_name, 'gitmate-test-user/test')

    def test_top_level_org(self):
        self.assertEqual(self.repo.top_level_org.name, 'gitmate-test-user')

    def test_last_pushed_at(self):
        self.assertEqual(self.repo.last_pushed_at,
                         datetime(2018, 4, 26, 9, 35, 17))

    def test_hoster(self):
        self.assertEqual(self.repo.hoster, 'gitlab')

    def test_full_name(self):
        self.assertEqual(self.repo.full_name, 'gitmate-test-user/test')

    def test_clone_url(self):
        self.assertEqual(self.repo.clone_url,
                         'https://{}@gitlab.com/gitmate-test-user/test.git'.format(
                             'oauth2:' + os.environ.get('GITLAB_TEST_TOKEN', ''))
                        )

    def test_get_labels(self):
        self.assertEqual(sorted(self.repo.get_labels()), ['a', 'b', 'c', 'dem'])

    def test_labels(self):
        with self.assertRaises(ElementAlreadyExistsError):
            self.repo.create_label('a', '#000000')

        with self.assertRaises(ElementDoesntExistError):
            self.repo.delete_label('f')

        self.repo.create_label('bug', '#000000')
        self.assertEqual(sorted(self.repo.get_labels()),
                         ['a', 'b', 'bug', 'c', 'dem'])
        self.repo.delete_label('bug')
        self.assertEqual(sorted(self.repo.get_labels()), ['a', 'b', 'c', 'dem'])

    def test_get_issue(self):
        self.assertEqual(self.repo.get_issue(1).title, 'new title')

    def test_get_mr(self):
        self.assertEqual(self.repo.get_mr(2).title, 'Sils/severalcommits')

    def test_create_issue(self):
        self.assertEqual(self.repo.create_issue(
            'title', 'body').title, 'title')

    def test_hooks(self):
        self.repo.register_hook('http://some.url/in/the/world', 'secret',
                                events={WebhookEvents.MERGE_REQUEST})
        self.assertIn('http://some.url/in/the/world', self.repo.hooks)
        # won't register again
        self.repo.register_hook('http://some.url/in/the/world')
        self.repo.delete_hook('http://some.url/in/the/world')
        self.assertNotIn('http://some.url/in/the/world', self.repo.hooks)
        # events not specified, register all
        self.repo.register_hook('http://some.url/in/the/world')
        self.assertIn('http://some.url/in/the/world', self.repo.hooks)
        self.repo.delete_hook('http://some.url/in/the/world')

    def test_filter_merge_request(self):
        self.assertEqual(len(self.repo.filter_merge_requests(state='all')), 42)
        self.assertEqual(len(self.repo.filter_merge_requests(state='opened')), 13)
        self.assertEqual(len(self.repo.filter_merge_requests(state='closed')), 25)
        self.assertEqual(len(self.repo.filter_merge_requests(state='merged')), 4)

    def test_merge_requests(self):
        self.assertEqual(len(self.repo.merge_requests), 13)

    def test_filter_issues(self):
        self.assertEqual(len(self.repo.filter_issues(state='all')), 22)
        self.assertEqual(len(self.repo.filter_issues(state='opened')), 20)
        self.assertEqual(len(self.repo.filter_issues(state='closed')), 2)
        self.assertEqual(len(self.repo.filter_issues(label='dem')), 2)
        self.assertEqual(
            len(self.repo.filter_issues(assignee='gitmate-test-user')), 3
        )

    def test_issues(self):
        self.assertEqual(len(self.repo.issues), 14)

    def test_create_fork(self):
        try:
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')
        except RuntimeError:
            fork = GitLabRepository(self.fork_token, 'gitmate-test-user-2/test')
            fork.delete()
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')

        self.assertIsInstance(fork, GitLabRepository)

    def test_delete_repo(self):
        try:
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')
        except RuntimeError:
            fork = GitLabRepository(self.fork_token, 'gitmate-test-user-2/test')
            fork.delete()
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')


        self.assertIsNone(fork.delete())

    def test_create_mr(self):
        try:
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')
        except RuntimeError:
            fork = GitLabRepository(self.fork_token, 'gitmate-test-user-2/test')
            fork.delete()
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')

        fork.create_file(path='.coafile', message='hello', content='hello', branch='master')
        mr = fork.create_merge_request(title='coafile', head='master', base='master',
                                       target_project_id=self.repo.data['id'],
                                       target_project=self.repo.data['path_with_namespace'])

        self.assertIsInstance(mr, GitLabMergeRequest)

    def test_create_file(self):
        try:
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')
        except RuntimeError:
            fork = GitLabRepository(self.fork_token, 'gitmate-test-user-2/test')
            fork.delete()
            fork = self.fork_repo.create_fork(namespace='gitmate-test-user-2')
        author = {
            'name': 'gitmate-test-user-2',
            'email': 'coafilecoala@gmail.com'
        }

        self.assertIsInstance(fork.create_file(path='.coafile', message='hello',
                                               content='hello', branch='master', author=author),
                              GitLabContent)

    def test_search_issues(self):
        created_after = datetime(2017, 6, 18).date()
        created_before = datetime(2017, 7, 15).date()
        issues = list(self.repo.search_issues(created_after=created_after,
                                              created_before=created_before,
                                              state=IssueStates.OPEN))
        self.assertEqual(len(issues), 2)
        issues = list(self.repo.search_issues(created_after=created_after,
                                              created_before=created_before,
                                              state=IssueStates.CLOSED))
        self.assertEqual(len(issues), 0)

    def test_search_mrs(self):
        updated_after = datetime(2017, 6, 18).date()
        updated_before = datetime(2017, 7, 2).date()
        merge_requests = list(self.repo.search_mrs(
            updated_after=updated_after,
            updated_before=updated_before,
            state=MergeRequestStates.OPEN))
        self.assertEqual(len(merge_requests), 1)
        merge_requests = list(self.repo.search_mrs(
            updated_after=updated_after,
            updated_before=updated_before,
            state=MergeRequestStates.CLOSED))
        self.assertEqual(len(merge_requests), 2)
        merge_requests = list(self.repo.search_mrs(
            updated_after=updated_after,
            updated_before=updated_before))
        self.assertEqual(len(merge_requests), 3)

    def test_commits(self):
        self.assertEqual({commit.sha for commit in self.repo.commits},
                         {'05a9faff56fd9bdb25d18a554bb2f3320de3fc6f',
                          '20d99d2b6124ccef9e9593749357a10c79085dae',
                          '2dfdc8f236fd5a4683ac52addb9d92b2920d6cfe',
                          '07434f75e2508d4e24f83f09c1735010b0c7e0b6',
                          'bd407435f5c16ee05f61aac5841e4cebe47f57a7',
                          'dd52e331780d30b58da030f9341abd07ba4ce31e',
                          '7747ee49b7d322e7d82520126ca275115aa67447',
                          'e3d12312ee8e4ba8e60ed009cf64fb3a1007b2c3',
                          '69e17e536092754e98aafbe5da0ee2be5fea81fb',
                          'e0fb5e9d7f6e0e362d61afb6f76974a0822f13eb',
                          '66fd5d82d0b9ed923e69198082222877611c8bce',
                          '33c53a63131beb1b06c10c4d3b2d7591338dbaa0',
                          '642d56a82f00feea4e63d31092c93f4a80a0273d',
                          '674498fd415cfadc35c5eb28b8951e800f357c6f',
                          '198dd16f8249ea98ed41876efe27d068b69fa215',
                          '515280bfe8488e1b403e0dd95c41a404355ca184',
                          'ed5fb0a1cc38a078a6f72b3523b6bce8c14be9b8',
                          '8ee108037431d696ec764859924475f5a0b42ad9',
                          '71a61579cb3aa493e8eadc9f183ff4377be4d1be',
                          'd6fe46331fcc32ac73c9308f94350d5822ce717d',
                          'cb9aa1c8964b3bcb0c542b281e06b339ddcc015f',
                          'ef46ed87766da84667570f28e04097fc3662ca86',
                          '6371fe50a92fa2147dcde0ce011db726b35b2646',
                          '3f49e40b56723a773c8d817a815c5a4a26115df7',
                          '99ba5b443787a2e5556136caabc91bfbdcb59780',
                          '645961c0841a84c1dd2a58535aa70ad45be48c46'})
        self.assertEqual({commit.sha
                          for commit in self.repo.filter_commits('sils')},
                         {'645961c0841a84c1dd2a58535aa70ad45be48c46'})
        repo = GitLabRepository(self.token, 'gitmate-test-user/empty')
        self.assertEqual(repo.commits, set())
        self.assertEqual(repo.filter_commits('sils'), set())
        self.assertEqual(repo.filter_commits('thisisarandomusernamewhichwillneverexist#killmeifitdoes'), None)

    def test_get_permission_level(self):
        sils = GitLabUser(self.token, 104269)
        user = GitLabUser(self.token)
        meetmangukiya = GitLabUser(self.token, 707601)
        noman = GitLabUser(self.token, 1)

        self.assertEqual(self.repo.get_permission_level(sils),
                         AccessLevel.ADMIN)
        self.assertEqual(self.repo.get_permission_level(user),
                         AccessLevel.ADMIN)
        self.assertEqual(self.repo.get_permission_level(meetmangukiya),
                         AccessLevel.CAN_WRITE)
        self.assertEqual(self.repo.get_permission_level(noman),
                         AccessLevel.CAN_VIEW)

    def test_parent(self):
        repo = GitLabRepository(self.token, 'nkprince007/test')
        self.assertEqual(repo.parent.full_name, 'gitmate-test-user/test')
        self.assertEqual(repo.parent.parent, None)

    def test_repo_create_and_delete(self):
        repo = GitLabRepository.create(self.token, 'test-repo')
        self.assertEqual(repo.full_name, 'gitmate-test-user/test-repo')
        self.assertIsNone(repo.delete())
        with self.assertRaises(RuntimeError):
            repo.refresh()
