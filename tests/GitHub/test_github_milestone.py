import os
#import datetime

from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubMilestone import GitHubMilestone
#from IGitt.GitHub.GitHubUser import GitHubUser
from IGitt.Interfaces import MilestoneStates
from IGitt.GitHub.GitHubRepository import GitHubRepository

from tests import IGittTestCase

class GitHubMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.milestone = GitHubMilestone.create(self.token, 'gitmate-test-user', 'test', 'IGitt Created Test Milestone')
        #self.milestone = GitHubMilestone(self.token, 'gitmate-test-user', 'test', 1)

    def test_setUp(self):
        assert(isinstance(self.milestone, GitHubMilestone))

    def test_number(self):
        self.assertEqual(self.milestone.number, 1)

    def test_title_getter(self):
        self.assertEqual(self.milestone.title, 'IGitt Created Test Milestone')

    def test_title_setter(self):
        self.milestone.title = 'Updated Title'
        self.assertEqual(self.milestone.title, 'Updated Title')

    def test_description_setter(self):
        self.milestone.description = 'Test Milestone Description'
        self.assertEqual(self.milestone.description, 'Test Milestone Description')

    def test_state_getter(self):
        self.assertEqual(self.milestone.state, MilestoneStates.OPEN)

    def test_close_method(self):
        self.milestone.close()
        self.assertEqual(self.milestone.state, 'closed')

    def test_project_getter(self):
        assert(isinstance(self.milestone.project, GitHubRepository))

    def tearDown(self):
        self.milestone.delete()
