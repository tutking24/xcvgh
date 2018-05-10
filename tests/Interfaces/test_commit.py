from unittest.mock import PropertyMock
from unittest.mock import patch

from IGitt.Interfaces.Repository import Repository
from IGitt.Interfaces.CommitStatus import Status
from IGitt.Interfaces.Commit import Commit

from tests import IGittTestCase


class TestCommit(IGittTestCase):

    def setUp(self):
        self.commit = Commit()
        self.repo = Repository()

    def test_status(self):
        CommitMock = type('CommitMock', (Commit, ),
                          {'set_status': lambda self, s: self.statuses.append(s),
                           'get_statuses': lambda self: self.statuses,
                           'statuses': []})

        commit = CommitMock()
        commit.pending()
        assert commit.get_statuses()[0].context == 'review/gitmate/manual'

        commit.ack()
        assert commit.get_statuses()[1].status == Status.SUCCESS
        commit.unack()
        assert commit.get_statuses()[2].status == Status.FAILED
        commit.pending()
        assert len(commit.get_statuses()) == 3

    @patch.object(Repository, 'hoster', new_callable=PropertyMock)
    @patch.object(Repository, 'full_name', new_callable=PropertyMock)
    @patch.object(Commit, 'repository', new_callable=PropertyMock)
    def test_get_keywords_issues(self, mock_repository, mock_full_name,
                                 mock_hoster):
        mock_hoster.return_value = 'github'
        mock_full_name.return_value = 'gitmate-test-user/test'
        mock_repository.return_value = self.repo

        test_cases = [
            ({('123', 'gitmate-test-user/test')},
             ['https://github.com/gitmate-test-user/test/issues/123']),
            ({('234', 'gitmate-test-user/test/repo')},
             ['gitmate-test-user/test/repo#234']),
            ({('345', 'gitmate-test-user/test')},
             ['gitmate-test-user/test#345']),
            ({('456', 'gitmate-test-user/test')},
             ['#456']),

            ({('345', 'gitmate-test-user/test')},
             ['hey there [#123](https://github.com/gitmate-test-user/test/issues/345)'])
        ]

        for expected, body in test_cases:
            self.assertEqual(
                self.commit.get_keywords_issues(r'', body),
                expected
            )

        bad = [
            '[#123]',
            '#123ds',
            'https://saucelabs.com/beta/tests/18c6aed24ed143d3bd1d1096498f34ac/commands#178',
        ]

        for body in bad:
            self.assertEqual(self.commit.get_keywords_issues(r'', body), set())
