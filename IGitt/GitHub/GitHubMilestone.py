"""
This contains the Milestone implementation for GitHub
"""

from IGitt.GitHub import GitHubMixin
from IGitt.Interfaces.Milestone import Milestone
from IGitt.GitHub import GitHubToken

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
        self._url = '/repos/{owner}/{project}/milestones/{milestone_number}'.format(owner=owner,
            project=project, milestone_number=number)
