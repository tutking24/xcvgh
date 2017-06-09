import unittest
import os

import vcr

from IGitt.GitLab.GitLabRepository import GitLabRepository
from IGitt import ElementAlreadyExistsError, ElementDoesntExistError

my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'],
                 filter_query_parameters=['private_token'],
                 filter_post_data_parameters=['private_token'])


class TestGitLabRepository(unittest.TestCase):

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo.yaml')
    def setUp(self):
        self.repo = GitLabRepository(os.environ.get('GITLAB_TEST_TOKEN', ''),
                                     'gitmate-test-user/test')

    def test_hoster(self):
        self.assertEqual(self.repo.hoster, 'gitlab')

    def test_full_name(self):
        self.assertEqual(self.repo.full_name, 'gitmate-test-user/test')

    def test_clone_url(self):
        self.assertEqual(self.repo.clone_url,
                         'https://{}@gitlab.com/gitmate-test-user/test.git'.format(
                             os.environ.get('GITLAB_TEST_TOKEN', ''))
                        )

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo_get_labels.yaml')
    def test_get_labels(self):
        self.assertEqual(sorted(self.repo.get_labels()), ['a', 'b', 'c', 'dem'])

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo_create_label.yaml')
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

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo_get_issue.yaml')
    def test_get_issue(self):
        self.assertEqual(self.repo.get_issue(1).title, 'new title')

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo_create_issue.yaml')
    def test_create_issue(self):
        self.assertEqual(self.repo.create_issue(
            'title', 'body').title, 'title')

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_repo_hooks.yaml')
    def test_hooks(self):
        self.repo.register_hook('http://some.url/in/the/world', '...')
        self.assertIn('http://some.url/in/the/world', self.repo.hooks)
        self.repo.register_hook('http://some.url/in/the/world')
        self.repo.delete_hook('http://some.url/in/the/world')
        self.assertNotIn('http://some.url/in/the/world', self.repo.hooks)