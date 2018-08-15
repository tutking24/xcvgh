"""
This module contains the TimeRecord class. The class is directly implented
within the interface since it doesnt communicate with GitHub or GitLab but uses
data which has been stored within IGitt already.
"""
from datetime import datetime
from datetime import timedelta
import re

from IGitt.Interfaces import IGittObject
from IGitt.Interfaces.User import User
from IGitt.Interfaces.Comment import Comment
from IGitt.Interfaces.Repository import Repository


class TimeRecord(IGittObject):
    def __init__(self, repository: Repository, comment_to_read_from: Comment):
        if comment_contains_time_record(comment_to_read_from):
            self._repository = repository
            self._id = comment_to_read_from.number
            self._date = comment_to_read_from.created
            self._loged_time = extract_loged_time_from_comment(
                comment_to_read_from)
            self._user = comment_to_read_from.author
        else:
            raise FaultyCommentError

    @property
    def date(self) -> datetime:
        """

        """
        return self._date

    @property
    def logged_time(self) -> timedelta:
        """

        """
        return self._logged_time

    @property
    def user(self) -> User:
        """

        """
        return self._user
