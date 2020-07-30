"""
    Note Data Access Object
"""
import abc
import datetime

from typing import Iterable

from work.scripts.app.models.note import Note


class NoteDAO(metaclass=abc.ABCMeta):
    """
        Abstract class for future DAO (Data Access Object) implementation
    """

    @abc.abstractmethod
    def create(self, note: Note):
        pass

    @abc.abstractmethod
    def update(self, note: Note):
        pass

    @abc.abstractmethod
    def delete(self, _id: int):
        pass

    @abc.abstractmethod
    def get_all(self) -> Iterable[Note]:
        pass

    @abc.abstractmethod
    def get_by_date(self, date: datetime.date) -> Note:
        pass

    @abc.abstractmethod
    def get_by_id(self, _id: int) -> Note:
        pass


class NoteNotFound(Exception):
    """
        Basic not found exception
    """
    pass
