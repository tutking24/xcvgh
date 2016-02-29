"""
Contains the Hoster implementation for Gitlab.
"""

from IGitt.Gitlab import query
from IGitt.Interfaces.Hoster import Hoster


class Gitlab(Hoster):
    """
    A high level interface to Gitlab.
    """

    def __init__(self, private_token):
        """
        Creates a new Gitlab Hoster object.

        :param private_token: A private token to use for authentication.
        """
        self._token = private_token

    @property
    def owned_repositories(self):
        """
        Retrieves repositories owned by the authenticated user.

        >>> from os import environ
        >>> gitlab = Gitlab(environ['GITLAB_TEST_TOKEN'])
        >>> gitlab.owned_repositories
        {'GitMate / someTest'}

        :return: A set of full repository names.
        """
        repo_list = query(self._token, 'projects/owned')
        return {repo['name_with_namespace'] for repo in repo_list}