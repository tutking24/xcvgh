import unittest
import os

import vcr

from IGitt.GitLab import GitLabOAuthToken
from IGitt.GitLab.GitLabOrganization import GitLabOrganization


my_vcr = vcr.VCR(match_on=['method', 'scheme', 'host', 'port', 'path'],
                 filter_query_parameters=['access_token'],
                 filter_post_data_parameters=['access_token'])


class GitLabOrganizationTest(unittest.TestCase):

    def setUp(self):
        self.token = GitLabOAuthToken(os.environ.get('GITLAB_TEST_TOKEN', ''))

        self.org = GitLabOrganization(self.token, 'gitmate-test-org')
        self.suborg = GitLabOrganization(self.token,
                                         'gitmate-test-org/subgroup')
        self.user = GitLabOrganization(self.token, 'gitmate-test-user')

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_organization_billable_users.yaml')
    def test_billable_users(self):
        # All users from all sub orgs plus the one from main org
        self.assertEqual(self.org.billable_users, 5)
        # Users from this sub org plus main org
        self.assertEqual(self.suborg.billable_users, 4)
        self.assertEqual(self.user.billable_users, 1)

    @my_vcr.use_cassette('tests/GitLab/cassettes/gitlab_organization_admins.yaml')
    def test_admins(self):
        self.assertEqual(self.suborg.owners, {'sils', 'nkprince007'})
        self.assertEqual(self.org.owners, {'sils', 'nkprince007'})
        self.assertEqual(self.user.owners, {'gitmate-test-user'})

    def test_organization(self):
        self.assertEqual(self.org.url,
                         'https://gitlab.com/gitmate-test-org')
        self.assertEqual(self.suborg.url,
                         'https://gitlab.com/gitmate-test-org/subgroup')
        self.assertEqual(self.user.url,
                         'https://gitlab.com/gitmate-test-user')