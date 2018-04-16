"""
This contains the Milestone implementation for GitHub
"""
from datetime import datetime

from IGitt.GitHub import GitHubMixin
from IGitt.Interfaces.Milestone import Milestone
from IGitt.GitHub import GitHubToken
from IGitt.Interfaces import post
from IGitt.Interfaces import patch
from IGitt.Interfaces import delete
from IGitt.Interfaces import get
from IGitt.GitHub.GitHubIssue import GitHubIssue
from IGitt.GitHub.GitHubMergeRequest import GitHubMergeRequest


class GitHubMilestone(GitHubMixin, Milestone):
    """
    This class represents a milestone on GitHub.
    """

    def __init__(self, token: GitHubToken, owner: str, project: str,
                 number: int):
        """
        Creates a new GitHubMilestone object with the given credentials.

        :param token: A Token object to be used for authentication.
        :param owner: The owner of the project
        :param project: The full name of the project.
        :param number: The milestones number.
        :raises RuntimeError: If something goes wrong (network, auth, ...)
        """
        self._token = token
        self._owner = owner
        self._project = project
        self._number = number
        self._url = '/repos/{owner}/{project}/milestones/{milestone_number}'\
            .format(owner=owner, project=project, milestone_number=number)

    @staticmethod
    def create(token: GitHubToken,
               owner: str,
               project: str,
               title: str,
               state: str = 'open',
               description: str = None,
               due_on: datetime = None):
        """
        Create a new milestone with given title
        :return: GitHubMilestone object of the newly created milestone.
        """
        url = '/repos/{owner}/{project}/milestones'.format(
            owner=owner, project=project)
        milestone = post(
            token, GitHubMilestone.absolute_url(url), {
                'title': title,
                'state': state,
                'description': description,
                'due_on': due_on
            })
        return GitHubMilestone.from_data(milestone, token, owner, project,
                                         milestone['number'])

    @property
    def number(self) -> int:
        """
        Returns the milestone "number" or id.
        """
        return self._number

    @property
    def title(self) -> str:
        """
        Retrieves the title of the milestone.
        """
        return self.data['title']

    @title.setter
    def title(self, new_title):
        """
        Sets the title of the milestone.

        :param new_title: The new title.
        """
        self.data = patch(self._token, self.url, {'title': new_title})

    @property
    def description(self) -> str:
        """
        Retrieves the main description of the milestone.
        """
        return self.data['description']

    @description.setter
    def description(self, new_description):
        """
        Sets the description of the milestone

        :param new_description: The new description .
        """
        self.data = patch(self._token, self.url,
                          {'description': new_description})

    @property
    def state(self):
        """
        Get's the state of the milestone.

        :return: Either IssueStates.OPEN or IssueStates.CLOSED.
        """
        return self.data['state']

    def close(self):
        """
        Closes the milestone.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = patch(self._token, self.url, {'state': 'closed'})

    def reopen(self):
        """
        Reopens the milestone.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = patch(self._token, self.url, {'state': 'open'})

    @property
    def created(self) -> datetime:
        """
        Retrieves a timestamp on when the milestone was created.
        """
        return self.data['created_at']

    @property
    def updated(self) -> datetime:
        """
        Retrieves a timestamp on when the milestone was updated the last time.
        """
        return self.data['updated_at']

    @property
    def due_date(self) -> datetime:
        """
        Retrieves a timestamp on when the milestone is due.
        """
        return self.data['due_on']

    @due_date.setter
    def due_date(self, new_date: datetime):
        """
        Sets the due date of the milestone.

        :param new_date: The new due date.
        """
        self.data = patch(self._token, self.url, {'due_on': new_date})

    def delete(self):
        """
        Deletes the milestone.
        This is not possible with GitLab api v4.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = delete(self._token, self.url)

    @property
    def group(self) -> str:
        """
        Retrieves the group this milestone belongs to.
        """
        return self._owner

    @property
    def issues(self) -> set:
        """
        Retrieves a set of issue objects that are assigned to this milestone.
        """
        self._issues_url = GitHubMixin.absolute_url(
            '/repos/{owner}/{project}/issues'.format(
                owner=self._owner, project=self._project))
        return {
            GitHubIssue.from_data(res, self._token, self._project,
                                  res['number'])
            for res in get(self._token, self._issues_url,
                           {'milestone': self._number})
            if 'pull_request' not in res
        }

    @property
    def merge_requests(self) -> set:
        """
        Retrieves a set of merge_request
        objects that are assigned to this milestone.
        """
        self._issues_url = GitHubMixin.absolute_url(
            '/repos/{owner}/{project}/issues'.format(
                owner=self._owner, project=self._project))
        return {
            GitHubMergeRequest.from_data(res, self._token, self._project,
                                         res['number'])
            for res in get(self._token, self._issues_url,
                           {'milestone': self._number})
            if 'pull_request' in res
        }
