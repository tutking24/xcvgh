import os

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabTeam import GitLabTeam

from tests import IGittTestCase


class GitLabTeamTest(IGittTestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))
        self.team = GitLabTeam(self.token, 1999111)

    def test_name(self):
        self.assertEqual(self.team.name, 'gitmate-test-org')

    def test_id(self):
        self.assertEqual(self.team.id, 1999111)

    def test_web_url(self):
        self.assertEqual(self.team.web_url,
                         'https://gitlab.com/groups/gitmate-test-org')

    def test_description(self):
        tm = GitLabTeam(self.token, 2614704)
        self.assertEqual(tm.description, 'This is a test subgroup')

    def test_members(self):
        self.assertEqual({user.username for user in self.team.members},
                         {'sils', 'gitmate-test-user', 'nkprince007'})

    def test_is_member(self):
        self.assertEqual(self.team.is_member('sils'), True)

    def test_get_organization(self):
        tm = GitLabTeam(self.token, 1999522)
        self.assertEqual(tm.get_organization.id, 1999111)
