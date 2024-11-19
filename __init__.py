"""
A program to encrypt and decrypt data stored in vaults
"""

import base64
import os
import sqlite3
import sys


try:
    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
except ImportError:
    print(
        "cryptography package is required to run the program\nKindly run `pip install cryptography` before starting me",
    )
    sys.exit(0)


class Constants:
    MY_BIRTH_DAY_UNIX_SECONDS = 860201400
    MY_BIRTH_DAY_BYTE_ARRAY = b"05 April 1997 AD"
    SALT = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"
    VAULT_DIR = os.path.join(os.getenv("USERPROFILE"), "Vault")
    VAULT_DB_FILE = os.path.join(VAULT_DIR, "master.db")


class Messages:
    VAULT_NOT_PRESENT = "Vault directory is not present at your home directory\nKindly create ~/Vault directory before starting me"
    INITIALIZING_VAULT = "Vault is empty, initializing new vault ..."
    ENTER_PASSWORD = "Enter the password for vault : "
    PASSWORD_VERIFICATION_SUCCESS = "Password verification success"
    PASSWORD_VERIFICATION_FAILURE = "Password verification failed"
    DB_FATAL_ERROR = "Fatal error occurred while accessing database, most likely due to corruption.\nKindly delete all files present in ~/Vault as they are tampered"
    DEC_FATAL_ERROR = "Fatal error occurred while decrypting data"
    WELCOME = "Welcome to your personal Vault !!!\nEnter ! to go back at any point"
    EXIT = "Thank you for using Vault !!!"

    ENTER_NAME = "Enter name : "
    ENTER_FILE = "Enter file location : "


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


class VaultCore:
    def __init__(self, password: str):
        kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)
        self.__fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
        self.__common_prefix = (
            b"\x80"
            + Constants.MY_BIRTH_DAY_UNIX_SECONDS.to_bytes(length=8, byteorder="big")
            + Constants.MY_BIRTH_DAY_BYTE_ARRAY
        )
        self.__common_prefix_len = len(self.__common_prefix)

    def encrypt_string(self, input: str) -> bytes:
        result = self.__fernet._encrypt_from_parts(
            input.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        )
        return base64.urlsafe_b64decode(result)[self.__common_prefix_len :]

    def decrypt_string(self, input: bytes) -> str:
        try:
            result = self.__fernet.decrypt(
                base64.urlsafe_b64encode(self.__common_prefix + input)
            )
            return result.decode()
        except InvalidToken:
            raise ValueError(Messages.DEC_FATAL_ERROR)

    def encrypt_bytes(self, input: bytes) -> bytes:
        result = self.__fernet._encrypt_from_parts(
            input,
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        )
        return base64.urlsafe_b64decode(result)[self.__common_prefix_len :]

    def decrypt_bytes(self, input: bytes) -> bytes:
        try:
            result = self.__fernet.decrypt(
                base64.urlsafe_b64encode(self.__common_prefix + input)
            )
            return result
        except InvalidToken:
            raise ValueError(Messages.DEC_FATAL_ERROR)


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


class Utils:
    @staticmethod
    def get_next_object_name(object_name: str = None) -> str:
        object_name_as_num = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            object_name_as_num[i] = ord(object_name[i]) - ord("a")

        for i in reversed(range(8)):
            if object_name_as_num[i] != 15:
                object_name_as_num[i] += 1
                break
            else:
                object_name_as_num[i] = 0

        result = [""] * 8
        for i in range(8):
            result[i] = chr(object_name_as_num[i] + ord("a"))

        return "".join(result)


from .operations import OperationsModule
