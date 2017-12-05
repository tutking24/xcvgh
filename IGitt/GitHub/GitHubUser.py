"""
Contains a representation of GitHub users.
"""
from typing import Optional, Iterator

from IGitt.GitHub import get
from IGitt.GitHub import GitHubMixin
from IGitt.GitHub import GitHubToken
from IGitt.GitHub.GitHubIssue import GitHubIssue
from IGitt.Interfaces.User import User


PREVIEW_HEADER = {'Accept': 'application/vnd.github.machine-man-preview+json'}


class GitHubUser(GitHubMixin, User):
    """
    A GitHub user, e.g. sils :)
    """
    def __init__(self, token: GitHubToken, username: Optional[str]=None):
        """
        Creates a GitHubUser with the given credentials.

        :param token:       The Oauth token.
        :param username:    The username of github user.
                            Takes None, if it's the associated user's token.
        """
        self._token = token
        self._url = '/users/' + username if username else '/user'
        self._username = username

    @property
    def username(self) -> str:
        """
        Retrieves the login for the user.
        """
        return self._username or self.data['login']

    @property
    def identifier(self) -> int:
        """
        Gets a unique id for the user that never changes.
        """
        return self.data['id']

    def installed_repositories(self, installation_id: int):
        """
        List repositories that are accessible to the authenticated user for an
        installation.
        """
        # Don't move to module code, causes circular dependencies
        from IGitt.GitHub.GitHubRepository import GitHubRepository

        repos = get(self._token, '/user/installations/{}/repositories'.format(
            installation_id), headers=PREVIEW_HEADER)['repositories']
        return {GitHubRepository.from_data(repo, self._token, repo['id'])
                for repo in repos}

    def assigned_issues(self, state='open') -> Iterator[GitHubIssue]:
        """
        Returns an iterator of all the issues that are assigned to the user.
        """
        from IGitt.GitHub.GitHubRepository import GitHubRepository

        yield from GitHubRepository._search(self._token,
                                            'is:issue state:{} assignee:{}'
                                            ''.format(state, self.username))
