import os

from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubTeam import GitHubTeam

from tests import IGittTestCase


class GitHubTeamTest(IGittTestCase):

    def setUp(self):
        self.token = GitHubToken(os.environ.get('GITHUB_TEST_TOKEN', ''))
        self.team = GitHubTeam(self.token, 2809871)

    def test_name(self):
        self.assertEqual(self.team.name, 'team')

    def test_id(self):
        self.assertEqual(self.team.id, 2809871)

    def test_web_url(self):
        self.assertEqual(self.team.web_url,
                         'https://github.com/orgs/gitmate-test-org/teams/team')

    def test_description(self):
        self.assertEqual(self.team.description,
                         'does nothing except for a bot to test with')

    def test_members(self):
        self.assertEqual({user.username for user in self.team.members},
                         {'nkprince007', 'Vamshi99', 'gitmate-test-user'})

    def test_is_member(self):
        self.assertEqual(self.team.is_member('Vamshi99'), True)
        self.assertEqual(self.team.is_member('sils'), False)

    def test_get_organization(self):
        self.assertEqual(self.team.get_organization.name, 'gitmate-test-org')
