"""
Holds the User class representing users on such a platform.
"""
from typing import Iterator
from typing import Set

from IGitt.Interfaces import IGittObject
from IGitt.Interfaces.Issue import Issue
from IGitt.Interfaces.Repository import Repository


class User(IGittObject):
    """
    Represents a user on GitHub/Lab. If you want to uniquely identify a user,
    use the `id` property as the id will never change while the username might.
    """

    @property
    def username(self) -> str:
        """
        The username of the user. Warning: this might change when the user
        renames himself!
        """
        raise NotImplementedError

    @property
    def identifier(self) -> int:
        """
        A unique ID used to identify the user. This is also given in oauth
        records.
        """
        raise NotImplementedError

    def installed_repositories(self,
                               installation_id: int) -> Set[Repository]:
        """
        List repositories that are accessible to the authenticated user for an
        installation.
        """
        raise NotImplementedError

    def assigned_issues(self) -> Iterator[Issue]:
        """
        Returns an iterator of all the issues that are assigned to the user.
        """
        raise NotImplementedError
