import os
#import datetime

from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubMilestone import GitHubMilestone
#from IGitt.GitHub.GitHubUser import GitHubUser
#from IGitt.Interfaces import IssueStates

from tests import IGittTestCase

class GitHubMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.milestone = GitHubMilestone.create(self.token, 'gitmate-test-user', 'test', 'IGitt Created Test Milestone')
        #self.milestone = GitHubMilestone(self.token, 'gitmate-test-user', 'test', 1)

    def test_setUp(self):
        assert(isinstance(self.milestone, GitHubMilestone))

    def tearDown(self):
        self.milestone.delete()

