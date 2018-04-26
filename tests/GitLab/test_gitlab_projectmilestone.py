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
        self.assertEqual(self.milestone.updated.day, datetime.datetime.utcnow().day)

    def test_project_getter(self):
        self.assertEqual(self.milestone.project, GitLabRepository(self.token, 'gitmate-test-user/test'))

    def tearDown(self):
        self.milestone.delete()
