from os import environ

from IGitt.Interfaces.Repository import WebhookEvents
from IGitt.Jira import JiraOAuth1Token
from IGitt.Jira.JiraRepository import JiraRepository

from tests import IGittTestCase


class JiraRepositoryTest(IGittTestCase):
    def setUp(self):
        self.token = JiraOAuth1Token(environ['JIRA_CLIENT_KEY'],
                                     environ['JIRA_TEST_TOKEN'],
                                     environ['JIRA_TEST_SECRET'])
        self.repo = JiraRepository(self.token, 'LTK')

    def test_identifier(self):
        self.assertEqual(self.repo.identifier, 10001)

    def test_web_url(self):
        self.assertEqual(self.repo.web_url,
                         'https://jira.gitmate.io:443/projects/LTK')

    def test_full_name(self):
        self.assertEqual(self.repo.full_name, 'Lasse Test Kanban')

    def test_get_issue(self):
        self.assertEqual(self.repo.get_issue(10001).title,
                         'Kanban boards are often divided into streams of work'
                         ', aka Swimlanes. By default, Kanban boards include '
                         'an "Expedite" swimlane for items marked with the '
                         'highest priority (like this one)')
    def test_hooks(self):
        self.assertEqual(self.repo.hooks, set())
        self.repo.register_hook('https://www.example.com',
                                events={WebhookEvents.ISSUE})
        self.repo.register_hook('https://www.example.com',
                                events={WebhookEvents.ISSUE})
        self.assertEqual(self.repo.hooks, {'https://www.example.com'})
        self.repo.delete_hook('https://www.example.com')
        self.assertEqual(self.repo.hooks, set())

    def test_issues(self):
        iss = self.repo.create_issue(
            'Task', 'Capture the Jedi', 'Kill the Jedi to win the war.')
        self.assertEqual(len(self.repo.issues), 18)
        iss.delete()
        self.assertEqual(len(self.repo.issues), 17)

    def test_create_and_delete(self):
        repo = JiraRepository.create(
            self.token, 'Test', 'software', 'TEX', 'nkprince007')
        repo.delete()
        with self.assertRaises(RuntimeError):
            repo.refresh()

    def test_parent(self):
        self.assertIsNone(self.repo.parent)
