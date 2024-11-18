"""
A program to encrypt and decrypt data stored in vaults
"""

import os
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
    FILE_FORMAT_NOTE = ".encnote"
    FILE_FORMAT_FILE = ".encfile"
    SALT = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"

    if os.name == "nt":
        SLASH = "\\"
        CLEAR_COMMAND = "cls"
    else:
        SLASH = "/"
        CLEAR_COMMAND = "clear"


class Messages:
    VAULT_NOT_PRESENT = "Vault directory is not present at your home directory\nKindly create ~/Vault directory before starting me"
    VAULT_NOT_EMPTY = "Vault cannot be verified and is not empty, hence all data are lost forever\nKindly delete all data present in ~/Vault and restart me"
    INITIALIZING_VAULT = "Vault is empty, initializing new vault ..."
    ENTER_PASSWORD = "Enter the password for vault : "
    VAULT_INITIALIZED = "Vault initialization completed"
    PASSWORD_VERIFICATION_FAILURE = "Password verification failed"
    WELCOME = "Welcome to your personal Vault !!!\nEnter ! to go back at any point"
    NOTES_OR_FILES = "Do you want to process notes or files (n, f) : "
    EXIT_VAULT = "Thank you for using Vault !!!"
    INVALID_OPTION = "Invalid option"
    NOTES_IN_VAULT = "Notes present in the vault :"
    FILES_IN_VAULT = "Files present in the vault :"
    READ_WRITE_OR_DELETE = "Do you want to read/write or delete (r, w, d) : "

    ENTER_NOTE_NAME = "Enter the note name : "
    NOTE_NOT_PRESENT = "Given note does not exist"
    NOTE_CREATED = "Note created successfully"
    NOTE_ALREADY_PRESENT = "Note already exists"
    NOTE_REMOVED = "Note removed successfully"

    ENTER_FILE_NAME = "Enter the file name : "
    ENTER_DIRECTORY_NAME = "Enter the directory name : "
    FILE_NOT_PRESENT = "File given does not exist"
    DIRECTORY_NOT_PRESENT = "Directory given does not exist"
    FILE_CREATED = "File created successfully"
    FILE_ALREADY_PRESENT = "File already exists"
    FILE_REMOVED = "File removed successfully"
