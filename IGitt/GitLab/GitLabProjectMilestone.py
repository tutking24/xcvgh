"""
This contains the Milestone implementation for GitLab
"""
from datetime import datetime
from urllib.parse import quote_plus

from IGitt.GitLab import GitLabMixin
from IGitt.GitLab import get
from IGitt.Interfaces import put
from IGitt.Interfaces import post
from IGitt.Interfaces import delete
from IGitt.GitLab import GitLabOAuthToken, GitLabPrivateToken
#from IGitt.Interfaces.Issue import Issue
from IGitt.Interfaces.Milestone import Milestone
from IGitt.GitLab.GitLabIssue import GitLabIssue
from IGitt.GitLab.GitLabMergeRequest import GitLabMergeRequest
import re


class GitLabProjectMilestone(GitLabMixin, Milestone):
    """
    This class represents a project level milestone on GitLab.
    This class does not support group level milestones.
    """

    def __init__(self, token: (GitLabOAuthToken, GitLabPrivateToken), project,
                 number: int):
        """
        Creates a new GitLabProjectMilestone with the given credentials.

        :param token: A Token object to be used for authentication.
        :param project: The full name of the project. Including the owner
                        e.g. ``owner/project``.
        :param number: The milestones identification number (id).
                        Not The clear text number given on the Web UI
        :raises RuntimeError: If something goes wrong (network, auth, ...)
        """
        self._token = token
        self._project = project
        self._id = number
        self._url = '/projects/{project}/milestones/{milestone_id}'.format(
            project=quote_plus(project), milestone_id=number)

    @staticmethod
    def create(
            token: (GitLabOAuthToken, GitLabPrivateToken),
            project,
            title: str,
            description: str = '',
    ):  # TODO: Add start_date and due_date
        """
        Create a new milestone with given title and body.

        >>> from os import environ
        >>> milestone = GitLabProjectMilestone.create(
        ...     GitLabOAuthToken(environ['GITLAB_TEST_TOKEN']),
        ...     'gitmate-test-user/test',
        ...     'test milestone title',
        ...     'sample description'
        ... )
        >>> milestone.state
        'active'

        Delete the milestone to avoid filling the test repo with milestones.

        >>> milestone.close()

        :return: GitLabProjectMilestone object of the newly created milestone.
        """
        url = '/projects/{project}/milestones'.format(
            project=quote_plus(project))
        milestone = post(token, GitLabProjectMilestone.absolute_url(url), {
            'title': title,
            'description': description
        })

        return GitLabProjectMilestone.from_data(milestone, token, project,
                                                milestone['id'])
        # TODO Commit and understand whats different now

    @property
    def number(self) -> int:
        """
        Returns the milestone "number" or id.
        """
        return self._id

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
        self.data = put(self._token, self.url, {'title': new_title})

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
        self.data = put(self._token, self.url,
                        {'description': new_description})

    @property
    def state(self):
        """
        Get's the state of the milestone.

        >>> from os import environ
        >>> milestone = GitLabProjectMilestone(GitLabOAuthToken(environ['GITLAB_TEST_TOKEN']),
        ...                     'gitmate-test-user/test', 1)
        >>> milestone.state
        'active'
#TODO create milestone to test against
        So if we close it:

        >>> milestone.close()
        >>> milestone.state
        'closed'

        And reopen it:

        >>> milestone.reopen()
        >>> milestone.state
        'active'

        :return: Either 'active' or 'closed'.
        """
        return self.data['state']

    def close(self):
        """
        Closes the milestone.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = put(self._token, self.url, {'state_event': 'close'})

    def reopen(self):
        """
        Reopens the milestone.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = put(self._token, self.url, {'state_event': 'activate'})

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
    def start_date(self) -> datetime:
        """
        Retrieves a timestamp on when the milestone was started.
        """
        return self.data['start_date']

    @start_date.setter
    def start_date(self, new_date: datetime):
        """
        Sets the start date of the milestone.

        :param new_date: The new start date.
        """
        self.data = put(self._token, self.url, {
            'start_date': new_date,
            'title': self.title
        })
        # The title is only set because the GitLab APIV4 requires this.

    @property
    def due_date(self) -> datetime:
        """
        Retrieves a timestamp on when the milestone is due.
        """
        return self.data['due_date']

    @due_date.setter
    def due_date(self, new_date: datetime):
        """
        Sets the due date of the milestone.

        :param new_date: The new due date.
        """
        self.data = put(self._token, self.url, {
            'due_date': new_date,
            'title': self.title
        })
        # The title is only set because the GitLab APIV4 requires this.

    def extract_repo_full_name(self, web_url):
        """
        Extracts the repository name from the web_url of the issue
        """
        return re.sub('https*://gitlab.com/|/issues/\d', '', web_url)

    @property
    def issues(self) -> set:
        """
        Retrieves a set of issue objects that are assigned to this milestone.
        """
        return {
            GitLabIssue.from_data(res, self._token,
                                  self.extract_repo_full_name(res['web_url']),
                                  res['iid'])
            for res in get(self._token, self.url + '/issues')
        }

    @property
    def merge_requests(self) -> set:
        """
        Retrieves a set of merge request objects that are assigned to this
        milestone.
        """
        return {
            GitLabMergeRequest.from_data(res, self._token,
                                         self.extract_repo_full_name(
                                             res['web_url']), res['iid'])
            for res in get(self._token, self.url + '/merge_requests')
        }

    def delete(self):
        """
        Deletes the milestone.
        This is not possible with GitLab api v4.

        :raises RuntimeError: If something goes wrong (network, auth...).
        """
        self.data = delete(self._token, self.url, self._id)
