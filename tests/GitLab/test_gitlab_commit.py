from datetime import datetime
import os

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabCommit import GitLabCommit
from IGitt.Interfaces.CommitStatus import CommitStatus
from IGitt.Interfaces.CommitStatus import Status

from tests import IGittTestCase


class GitLabCommitTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.commit = GitLabCommit(self.token,
                                   'gitmate-test-user/test',
                                   '3fc4b860e0a2c17819934d678decacd914271e5c')

    def test_sha(self):
        self.assertIn('3fc4b86', self.commit.sha)

    def test_pushed_at(self):
        self.assertEqual(self.commit.pushed_at,
                         datetime(2016, 1, 24, 17, 49, 12))

    def test_message(self):
        self.assertEqual(self.commit.message, 'Update README.md')

    def test_repository(self):
        self.assertEqual(self.commit.repository.full_name,
                         'gitmate-test-user/test')

    def test_parent(self):
        self.assertEqual(self.commit.parent.sha,
                         '674498fd415cfadc35c5eb28b8951e800f357c6f')

    def test_set_status(self):
        commit = GitLabCommit(self.token,
                              'gitmate-test-user/test',
                              '3fc4b860e0a2c17819934d678decacd914271e5c')
        status = CommitStatus(Status.FAILED, 'Theres a problem', 'gitmate/test')
        self.commit.set_status(status)
        self.assertEqual(commit.get_statuses(
            ).pop().description, 'Theres a problem')

    def test_combined_status(self):
        self.assertEqual(self.commit.combined_status, Status.FAILED)
        commit = GitLabCommit(self.token,
                              'gitmate-test-user/test',
                              'a37bb904b39a4aabee24f52ff98a0a988a41a24a')
        self.assertEqual(commit.combined_status, Status.PENDING)
        commit = GitLabCommit(self.token,
                              'gitmate-test-user/test',
                              '9ba5b704f5866e468ec2e639fa893ae4c129f2ad')
        self.assertEqual(commit.combined_status, Status.SUCCESS)

    def test_get_patch_for_file(self):
        patch = self.commit.get_patch_for_file('README.md')
        self.assertEqual(patch, '@@ -1,2 +1,4 @@\n'
                                ' # test\n'
                                ' a test repo\n'
                                '+\n'
                                '+a tst pr\n')

    def test_comment(self):
        self.commit = GitLabCommit(self.token,
                                   'gitmate-test-user/test',
                                   '3fc4b860e0a2c17819934d678decacd914271e5c')
        # commit comments cannot be retrieved
        self.assertIsNone(self.commit.comment('An issue is here'))
        self.assertIsNone(self.commit.comment("Here in line 4, there's a spelling mistake!",
                                              'README.md', 4))
        self.assertIsNone(self.commit.comment("Here in line 4, there's a spelling mistake!",
                                              'README.md', 4, mr_number=6))
        self.assertIsNone(self.commit.comment('test comment', 'READNOT.md', 4))
        # MR comments can be retrieved
        self.assertEqual(self.commit.comment('test comment', 'READNOT.md', mr_number=6).body,
                         'Comment on 3fc4b860e0a2c17819934d678decacd914271e5c, file READNOT.md.\n\n'
                         'test comment')


    def test_unified_diff(self):
        self.assertEqual(self.commit.unified_diff,
                         '--- a/README.md\n'
                         '+++ b/README.md\n'
                         '@@ -1,2 +1,4 @@\n'
                         ' # test\n'
                         ' a test repo\n'
                         '+\n'
                         '+a tst pr\n')

    def test_closes_issues(self):
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '9ba5b704f5866e468ec2e639fa893ae4c129f2ad')
        self.assertEqual({int(issue.number) for issue in commit.closes_issues},
                         {21, 22, 23, 26, 27, 30})

    def test_mentioned_issues(self):
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '9ba5b704f5866e468ec2e639fa893ae4c129f2ad')
        self.assertEqual({int(issue.number) for issue in commit.mentioned_issues},
                         {21, 22, 23, 31, 26, 27, 30})

    def test_will_fix_issues(self):
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '0164595c7d75404c2e0ce8622cea825e59e9d558')
        self.assertEqual({int(issue.number)
                          for issue in commit.will_fix_issues},
                         {21, 22, 26, 27, 30})
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '38715b42c86ec565a6e0e4b13255448e8f202f8d')
        self.assertEqual(commit.will_fix_issues, set())

    def test_will_close_issues(self):
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '0164595c7d75404c2e0ce8622cea825e59e9d558')
        self.assertEqual({int(issue.number)
                          for issue in commit.will_close_issues},
                         {23})
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '38715b42c86ec565a6e0e4b13255448e8f202f8d')
        self.assertEqual(commit.will_close_issues, set())

    def test_will_resolve_issues(self):
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '0164595c7d75404c2e0ce8622cea825e59e9d558')
        self.assertEqual({int(issue.number)
                          for issue in commit.will_resolve_issues},
                         {41})
        commit = GitLabCommit(self.token, 'gitmate-test-user/test',
                              '38715b42c86ec565a6e0e4b13255448e8f202f8d')
        self.assertEqual(commit.will_resolve_issues, set())
