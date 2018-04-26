import os
import datetime

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabProjectMilestone import GitLabProjectMilestone
#from IGitt.GitLab.GitLabUser import GitLabUser
from IGitt.Interfaces import MilestoneStates
from IGitt.GitLab.GitLabRepository import GitLabRepository

from tests import IGittTestCase

class GitLabProjectMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.milestone = GitLabProjectMilestone(self.token, 'gitmate-test-user/test', 513937)

    def test_setUp(self):
        assert(isinstance(self.milestone, GitLabProjectMilestone))

    def test_number_getter(self):
        self.assertEqual(self.milestone.number, 513937)

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
        self.assertEqual(self.milestone.created, datetime.datetime(2018, 4, 25, 9, 11, 0, 29000))

    def test_updated_getter(self):
        self.milestone.description = 'Description update to test updated getter'
        self.assertEqual(self.milestone.updated.date(), datetime.datetime(2018, 4, 26).date())
        self.milestone.description = None

    def test_due_date_setter(self):
        self.milestone.due_date = datetime.datetime(2050, 4, 23, 0, 0)
        self.assertEqual(self.milestone.due_date, datetime.datetime(2050, 4, 23, 0, 0))
        self.milestone.due_date = None
        self.assertEqual(self.milestone.due_date, None)

    def test_start_date_setter(self):
        self.milestone.start_date = datetime.datetime(2040, 4, 23, 0, 0)
        self.assertEqual(self.milestone.start_date, datetime.datetime(2040, 4, 23, 0, 0))
        self.milestone.start_date = None
        self.assertEqual(self.milestone.start_date, None)

    def test_issues_getter(self):
        self.assertEqual({int(issue.number) for issue in self.milestone.issues},
                         {37, 38, 39}) # Prüft nicht, ob ein set zurück kommt?

    def test_merge_requests_getter(self):
        self.assertEqual({int(merge_request.number) for merge_request in self.milestone.merge_requests},
                         {76})

    def test_project_getter(self):
        assert(isinstance(self.milestone.project, GitLabRepository))

    def test_create_delete_methods(self):
        self.minimal_data_milestone = GitLabProjectMilestone.create(self.token, 'gitmate-test-user/test', 'Temporary created minimal data test milestone.')
        assert(isinstance(self.minimal_data_milestone, GitLabProjectMilestone))
        self.assertEqual(self.minimal_data_milestone.title, 'Temporary created minimal data test milestone.')
        self.minimal_data_milestone.delete()

        self.full_data_milestone = GitLabProjectMilestone.create(self.token, 'gitmate-test-user/test', 'Temporary created full data test milestone.', 'Test Description', datetime.datetime(2050, 4, 23), datetime.datetime(2040, 4, 23))
        assert(isinstance(self.full_data_milestone, GitLabProjectMilestone))
        self.assertEqual(self.full_data_milestone.start_date, datetime.datetime(2040, 4, 23))
        self.full_data_milestone.delete()
