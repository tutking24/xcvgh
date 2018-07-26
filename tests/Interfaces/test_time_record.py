import os
from datetime import timedelta

from IGitt.Interfaces import TimeRecord
from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabComment import GitLabComment
from IGitt.Interfaces.Comment import CommentType

from tests import IGittTestCase


class TestTimeRecord(IGittTestCase):
    def setUp(self):
        token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.time_subtracting_comment = GitLabComment(
            token, 'gitmate-test-user/test', 42, CommentType.ISSUE, 88185697)
        self.time_adding_comment = GitLabComment(
            token, 'gitmate-test-user/test', 42, CommentType.ISSUE, 88185691)
        self.time_reseting_comment = GitLabComment(
            token, 'gitmate-test-user/test', 42, CommentType.ISSUE, 88178597)
        self.comment_without_time_record = GitLabComment(
            token, 'gitmate-test-user/test', 42, CommentType.ISSUE, 88744093)
        self.comment_with_several_values = GitLabComment(
            token, 'gitmate-test-user/test', 42, CommentType.ISSUE, 88178603)

    def test_comment_contains_time_record(self):
        self.assertTrue(
            TimeRecord.comment_contains_time_record(
                self.time_subtracting_comment))
        self.assertTrue(
            TimeRecord.comment_contains_time_record(self.time_adding_comment))
        self.assertTrue(
            TimeRecord.comment_contains_time_record(
                self.time_reseting_comment))
        self.assertFalse(
            TimeRecord.comment_contains_time_record(
                self.comment_without_time_record))

    def test_extract_loged_time_from_comment(self):
        self.assertEqual(
            TimeRecord.extract_loged_time_from_comment(
                self.time_subtracting_comment),
            timedelta(minutes=-1))
        self.assertEqual(
            TimeRecord.extract_loged_time_from_comment(
                self.time_adding_comment),
            timedelta(minutes=1))
        self.assertEqual(
            TimeRecord.extract_loged_time_from_comment(
                self.comment_with_several_values),
            timedelta(seconds=20, minutes=13, hours=1))
        #TODO: Add test for time_reseting_comment
