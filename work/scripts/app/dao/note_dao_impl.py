"""
    NoteDAO Implementation
"""
import datetime
from typing import Iterable

from work.scripts.app.config import config
from work.scripts.app.models.note import Note
from work.scripts.app.dao.note_dao import NoteDAO

from work.scripts.app.config import BASE_DIR


class NoteDAOImpl(NoteDAO):
    """
        Implementation for abstract class
    """

    DB_NAME = 'notes'

    def __init__(self, connection):
        """
            Constructor
            Initializes database if dont exist
            :param connection: Database connection
        """
        self.connection = connection

        schema_path = config['paths']['schemas']

        self.init_db(schema_path)

    def create(self, note: Note):
        """
        Implementation for abstract method

        :param note: given note
        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO notes (date, name, description) VALUES (?, ?, ?)""",
            tuple(str(x) for x in note.__dict__.values())[:-1:]
        )

    def update(self, note: Note):
        """
        Implementation for abstract method

        :param note: given note
        :return: Updated note
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE notes SET name = (?), description = (?) WHERE uuid = (?)""",
            (note.name, note.description, note.uuid,)
        )

    def delete(self, _id: int):
        """
        Implementation for abstract method

        :param _id: given uuid
        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute("""DELETE FROM notes WHERE uuid = (?)""", (_id,))

    def get_all(self) -> Iterable:
        """
        Implementation for abstract method

        :return: Iterable of Notes
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM notes""")
        return cursor.fetchall()

    def get_by_date(self, date: datetime.date) -> Iterable[Note]:
        """
        Implementation for abstract method

        :return: Iterable of Notes
        """

        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM notes WHERE date = (?)""", (str(date),))
        return list([Note(*x) for x in cursor.fetchall()])

    def get_by_id(self, _id: int) -> Note:
        """
        Implementation for abstract method

        :param _id: requested id
        :return: fetched Note
        """
        cursor = self.connection.cursor()
        cursor.execute("""SELECT * FROM notes WHERE uuid = (?)""", (_id,))
        return Note(*cursor.fetchone())

    def init_db(self, schema_path):
        """
        Creates database from given schema if not exist

        :param schema_path: Path to sql file with associated schema
        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute(open(str(BASE_DIR.absolute()) + schema_path, 'r').read())

    def __exit__(self, exc_type, exc_val, exc_tb):
        cursor = self.connection.cursor()
        cursor.close()
