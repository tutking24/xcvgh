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


def comment_contains_time_record(comment_to_read_from: Comment):

    if (re.match(r'(subtracted|added)(\s\d+[wdhms]){1,5}(\sof time spent$)',
                 comment_to_read_from.data['body'])
            or comment_to_read_from.data['body'] == 'removed time spent'):
        return True


def extract_loged_time_from_comment(
        comment_to_read_from: Comment) -> timedelta:

    if re.match(r'(subtracted|added)(\s\d+[wdhms]){1,5}(\sof time spent$)',
                comment_to_read_from.data['body']):

        time_values = {'s': 0, 'm': 0, 'h': 0, 'd': 0, 'w': 0}

        for time_unit in ['s', 'm', 'h', 'd', 'w']:
            time_extraction_regex = r'(?:\s)(\d+)(?:' + time_unit + r')'

            if not re.search(time_extraction_regex,
                             comment_to_read_from.data['body']):
                pass

            else:
                time_values[time_unit] = int(
                    re.search(time_extraction_regex,
                              comment_to_read_from.data['body']).group(1))

        extracted_time = timedelta(
            seconds=time_values['s'],
            minutes=time_values['m'],
            hours=time_values['h'],
            days=time_values['d'],
            weeks=time_values['w'])

    if re.search(r'(^subtracted)', comment_to_read_from.data['body']):
        extracted_time = extracted_time * (-1)

    #TODO: Extract reset somehow?
    return extracted_time


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
    def loged_time(self) -> timedelta:
        """

        """
        return self._loged_time

    @property
    def user(self) -> User:
        """

        """
        return self._user
