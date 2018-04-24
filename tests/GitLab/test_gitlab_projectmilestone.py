import os
import datetime

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabProjectMilestone import GitLabProjectMilestone

from tests import IGittTestCase

class GitLabProjectMilestoneTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.milestone = GitLabProjectMilestone.create(self.token, 'gitmate-test-user/test', 'For IGitt tests created test milestone NEW TITEL')
        self.day_created = datetime.datetime.utcnow().day # Gets a datetime object of the day of the creation

    def test_setUp(self):
        assert(isinstance(self.milestone, GitLabProjectMilestone))


    def tearDown(self):
        self.milestone.delete()
