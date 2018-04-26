import os
import datetime
import pytest

from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubMilestone import GitHubMilestone
#from IGitt.GitHub.GitHubUser import GitHubUser
from IGitt.Interfaces import MilestoneStates
from IGitt.GitHub.GitHubRepository import GitHubRepository

from tests import IGittTestCase

class GitHubMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.milestone = GitHubMilestone(self.token, 'gitmate-test-user', 'test', 1)

    def test_setUp(self):
        assert(isinstance(self.milestone, GitHubMilestone))

    def test_number(self):
        self.assertEqual(self.milestone.number, 1)

    def test_title_getter(self):
        self.assertEqual(self.milestone.title, 'Permanent IGitt test milestone. DO NOT DELETE.')

    def test_title_setter(self):
        self.milestone.title = 'Updated Title'
        self.assertEqual(self.milestone.title, 'Updated Title')
        self.milestone.title = 'Permanent IGitt test milestone. DO NOT DELETE.'

    def test_description_setter(self):
        self.milestone.description = 'Test Milestone Description'
        self.assertEqual(self.milestone.description, 'Test Milestone Description')
        self.milestone.description = None

    def test_state_getter(self):
        self.assertEqual(self.milestone.state, MilestoneStates.OPEN)

    def test_close_reopen_methods(self):
        self.milestone.close()
        self.assertEqual(self.milestone.state, MilestoneStates.CLOSED)

        self.milestone.reopen()
        self.assertEqual(self.milestone.state, MilestoneStates.OPEN)

    def test_created_getter(self):
        self.assertEqual(self.milestone.created, datetime.datetime(2018, 4, 24, 12, 19, 49))


    def test_updated_getter(self):
        self.milestone.description = 'Description update to test updated getter'
        self.assertEqual(self.milestone.updated.date(), datetime.datetime(2018, 4, 25).date())
        self.milestone.description = None

    def test_due_date_setter(self):
        self.milestone.due_date = datetime.datetime(2050, 4, 23, 7)
        self.assertEqual(self.milestone.due_date, datetime.datetime(2050, 4, 23, 7))
        self.milestone.due_date = None
        self.assertEqual(self.milestone.due_date, None)

    def test_issues_getter(self):
        self.assertEqual({int(issue.number) for issue in self.milestone.issues},
                         {136, 138, 139}) # Prüft nicht, ob ein set zurück kommt?

    def test_merge_requests_getter(self):
        self.assertEqual({int(merge_request.number) for merge_request in self.milestone.merge_requests},
                         {140})

    def test_start_date_getter(self):
        self.assertEqual(self.milestone.start_date, None)

    def test_project_getter(self):
        assert(isinstance(self.milestone.project, GitHubRepository))

