"""
This module contains the TimeRecord class. The class is directly implented
within the interface since it doesnt communicate with GitHub or GitLab but uses
data which has been stored within IGitt already.
"""
from datetime import datetime
from datetime import timedelta

from IGitt.Interfaces.User import User


class TimeRecord(IGittObject):

    @property
    def date(self) -> datetime:
        """

        """
        raise NotImplementedError

    @property
    def loged_time(self) -> timedelta:
        """

        """
        raise NotImplementedError

    @property
    def user(self) -> User:
        """

        """
        raise NotImplementedError
