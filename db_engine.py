import sqlite3

from . import Messages


class Queries:
    GET_NOTES = "SELECT id, name FROM files WHERE type = 'note'"
    GET_FILES = "SELECT id, name FROM files WHERE type = 'file'"

    GET_NOTE_ID = "SELECT id FROM files WHERE type = 'note' AND name = ?"
    GET_FILE_ID = "SELECT id FROM files WHERE type = 'file' AND name = ?"
    GET_OBJECTS = "SELECT id, page, name FROM objects WHERE file_id = ?"

    INSERT_NOTE = "INSERT INTO files(name, type) VALUES(?, 'note')"
    INSERT_FILE = "INSERT INTO files(name, type) VALUES(?, 'file')"
    INSERT_OBJECT = "INSERT INTO objects(file_id, page, name) VALUES(?, ?, ?)"

    DEL_FILE = "DELETE FROM files WHERE id = ?"
    DEL_OBJECT = "DELETE FROM objects WHERE id = ?"


class DBEngine:
    def __init__(self, db_file: str):
        self.__db_connection = sqlite3.connect(db_file)
        self.__db_cursor = self.__db_connection.cursor()

    def create_tables(self):
        self.__db_cursor.execute(
            "CREATE TABLE reference (name TEXT PRIMARY KEY, value TEXT)"
        )
        self.__db_cursor.execute(
            "CREATE TABLE files (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, "
            "UNIQUE(name, type)"
            ")"
        )
        self.__db_cursor.execute(
            "CREATE TABLE objects (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER, page INTEGER, name TEXT UNIQUE, "
            "FOREIGN KEY(file_id) REFERENCES files(id)"
            ")"
        )

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        try:
            result_cursor = self.__db_cursor.execute(query, params)
            self.__db_connection.commit()
            return result_cursor
        except sqlite3.Error as e:
            if e.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                raise RuntimeError(e.sqlite_errorname)
            else:
                raise RuntimeError(Messages.DB_FATAL_ERROR)

    def _is_present(self, name: str, type: str):
        if type == "note":
            result = self.execute(Queries.GET_NOTE_ID, (name,)).fetchone()
        elif type == "file":
            result = self.execute(Queries.GET_FILE_ID, (name,)).fetchone()

        if result is None:
            raise RuntimeError("NO_DATA_FOUND")

    def is_note_present(self, name: str):
        self._is_present(name, "note")

    def is_file_present(self, name: str):
        self._is_present(name, "file")

    def get_reference(self, name: str):
        result = self.execute(
            "SELECT value FROM reference WHERE name = ?", (name,)
        ).fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def put_reference(self, name: str, value):
        if self.get_reference(name) is None:
            self.execute(
                "INSERT INTO reference(name, value) VALUES(?, ?)", (name, value)
            )
        else:
            self.execute("UPDATE reference SET value = ? WHERE name = ?", (value, name))

    def close(self):
        self.__db_cursor.close()
        self.__db_connection.close()
