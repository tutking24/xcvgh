import os
import datetime
from datetime import timedelta
import pytest

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabIssue import GitLabIssue
from IGitt.GitLab.GitLabUser import GitLabUser
from IGitt.Interfaces import IssueStates
from IGitt.GitLab.GitLabProjectMilestone import GitLabProjectMilestone

from tests import IGittTestCase


class GitLabIssueTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.iss = GitLabIssue(self.token,
                               'gitmate-test-user/test', 3)

    def test_repo(self):
        self.assertEqual(self.iss.repository.full_name,
                         'gitmate-test-user/test')

    def test_title(self):
        self.iss.title = 'new title'
        self.assertEqual(self.iss.title, 'new title')

    def test_assignee(self):
        self.assertEqual(self.iss.assignees, set())
        iss = GitLabIssue(self.token,
                          'gitmate-test-user/test', 27)

        user = GitLabUser(self.token, 707601)
        iss.assign(user)
        self.assertEqual(iss.assignees, {user})
        iss.unassign(user)
        self.assertEqual(iss.assignees, set())
        iss = GitLabIssue(self.token, 'gitmate-test-user/test', 2)
        self.assertEqual(iss.assignees, set())
        self.assertEqual(len(iss.available_assignees), 5)

    def test_number(self):
        self.assertEqual(self.iss.number, 3)

    def test_description(self):
        self.iss.description = 'new description'
        self.assertEqual(self.iss.description, 'new description')

    def test_author(self):
        self.assertEqual(self.iss.author.username, 'gitmate-test-user')

    def test_add_comment(self):
        self.iss.add_comment('this is a test comment')
        self.assertEqual(self.iss.comments[0].body, 'this is a test comment')

    def test_issue_labels(self):
        self.iss.labels = set()
        self.assertEqual(self.iss.labels, set())
        self.iss.labels = self.iss.labels | {'dem'}
        self.iss.labels = self.iss.labels  # Doesn't do a request :)
        self.assertEqual(len(self.iss.available_labels), 4)
        self.assertEqual(len(self.iss.labels), 1)

    def test_time(self):
        self.assertEqual(self.iss.created,
                         datetime.datetime(2017, 6, 5, 6, 19, 6, 379000))
        self.assertEqual(self.iss.updated,
                         datetime.datetime(2017, 9, 24, 17, 6, 45, 955000))

    def test_state(self):
        self.iss.close()
        self.assertEqual(self.iss.state, IssueStates.CLOSED)
        self.assertEqual(str(self.iss.state), 'closed')
        self.iss.reopen()
        self.assertEqual(self.iss.state, IssueStates.OPEN)
        self.assertEqual(str(self.iss.state), 'open')

    def test_issue_create(self):
        issue = GitLabIssue.create(self.token,
                                   'gitmate-test-user/test',
                                   'test title', 'test body')
        self.assertEqual(issue.state, IssueStates.OPEN)
        issue.delete()

    def test_description_is_string(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 23)
        issue.data['description'] = None
        self.assertEqual(issue.description, '')

    def test_reactions(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 23)
        self.assertEqual(sorted([r.name for r in issue.reactions]),
                         ['golf', 'thumbsdown', 'thumbsup'])

    def test_weight(self):
        self.iss.weight = 5
        self.assertEqual(self.iss.weight, 5)

    def test_mrs_closed_by(self):
        issue = GitLabIssue(self.token, 'coala/package_manager', 152)
        self.assertEqual({int(i.number) for i in issue.mrs_closed_by}, {98})

    def test_milestone_setter(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)
        self.assertEqual(issue.milestone, None)
        issue.milestone = GitLabProjectMilestone(
            self.token, 'gitmate-test-user/test', 513937)
        self.assertEqual(issue.milestone.title,
                         'Permanent IGitt test milestone. DO NOT DELETE.')
        issue.milestone = None
        self.assertEqual(issue.milestone, None)

    def test_time_estimate_getter(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)
        self.assertEqual(issue.time_estimate, timedelta(seconds=7320))

    def test_time_estimate_setter(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)

        issue.time_estimate = None
        self.assertEqual(issue.time_estimate, timedelta(seconds=0))
        issue.time_estimate = timedelta(seconds=0)
        self.assertEqual(issue.time_estimate, timedelta(seconds=0))

        issue.time_estimate = timedelta(minutes=1)
        self.assertEqual(issue.time_estimate, timedelta(seconds=60))

        issue.time_estimate = timedelta(seconds=7320)
        self.assertEqual(issue.time_estimate, timedelta(seconds=7320))

    def test_total_time_spent_getter(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))

    def test_total_time_spent_setter(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)

        # Writing absolute values
        issue.total_time_spent = timedelta(seconds=6600)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=6600))
        with pytest.raises(RuntimeError):
            issue.total_time_spent = timedelta(seconds=-1)

        # Different time units
        issue.time_estimate = timedelta(minutes=1)
        self.assertEqual(issue.time_estimate, timedelta(seconds=60))

        # Reseting
        issue.total_time_spent = None
        self.assertEqual(issue.total_time_spent, timedelta(seconds=0))
        issue.total_time_spent = timedelta(seconds=0)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=0))

        # Restoring original value
        issue.total_time_spent = timedelta(seconds=4400)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))

    def test_add_to_total_time_spent(self):
        issue = GitLabIssue(self.token, 'gitmate-test-user/test', 42)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))

        # Writing relative values
        issue.add_to_total_time_spent(timedelta(seconds=1))
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4401))
        issue.add_to_total_time_spent(timedelta(seconds=-1))
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))

        # Different time units
        issue.add_to_total_time_spent(timedelta(minutes=1))
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4460))
        issue.add_to_total_time_spent(timedelta(minutes=-1))
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))

        # Adding nothing
        issue.add_to_total_time_spent = None
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))
        issue.add_to_total_time_spent = timedelta(seconds=0)
        self.assertEqual(issue.total_time_spent, timedelta(seconds=4400))
