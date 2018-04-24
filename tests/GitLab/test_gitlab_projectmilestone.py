import os
import datetime

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabProjectMilestone import GitLabProjectMilestone
from IGitt.Interfaces import MilestoneStates
from IGitt.GitLab.GitLabRepository import GitLabRepository

from tests import IGittTestCase

class GitLabProjectMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.milestone = GitLabProjectMilestone.create(self.token, 'gitmate-test-user/test', 'For IGitt tests created test milestone NEW TITEL')
        self.day_created = datetime.datetime.utcnow().day # Gets a datetime object of the day of the creation

    def test_setUp(self):
        assert(isinstance(self.milestone, GitLabProjectMilestone))

    def test_number_getter(self):
        self.preset_milestone = GitLabProjectMilestone(self.token, 'gitmate-test-user/test', 345808)
        self.assertEqual(self.preset_milestone.number, 345808)

    def test_title_setter(self):
        self.milestone.title = 'Test title in test_title_setter'
        self.assertEqual(self.milestone.title, 'Test title in test_title_setter')

    def test_description_setter(self):
        self.milestone.description = 'Test description in test_description_setter'
        self.assertEqual(self.milestone.description, 'Test description in test_description_setter')

    def test_state_getter(self):
        self.assertEqual(self.milestone.state, MilestoneStates.OPEN)

    def test_created_getter(self):
        self.assertEqual(self.milestone.created.day, self.day_created)

    def test_updated_getter(self):
        self.milestone.description = 'Description update to test updated getter'
        self.assertEqual(self.milestone.updated.day, datetime.datetime.utcnow().day)

    def test_project_getter(self):
        self.assertEqual(self.milestone.project, GitLabRepository(self.token, 'gitmate-test-user/test'))

    def tearDown(self):
        self.milestone.delete()
