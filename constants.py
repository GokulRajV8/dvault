import os


class Constants:
    APP_VERSION = "0.1"
    MY_BIRTH_DAY_UNIX_SECONDS = 860201400
    MY_BIRTH_DAY_BYTE_ARRAY = b"05 April 1997 AD"
    SALT = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"
    VAULT_DIR = os.path.join(os.getenv("USERPROFILE"), "Vault")
    VAULT_DB_FILE = os.path.join(VAULT_DIR, "master.db")
    OBJ_NAME_CHAR_START = "a"
    OBJ_NAME_CHAR_COUNT = 15
    OBJ_NAME_LEN = 8
    VERIFIER_STRING = "success"
    ENTRY_TYPE_NOTES = "Notes"
    ENTRY_TYPE_FILES = "Files"

    OPTION_NOTES = "n"
    OPTION_FILES = "f"
    OPTION_READ = "r"
    OPTION_WRITE = "w"
    OPTION_DELETE = "d"
    OPTION_YES = "y"
    OPTION_NO = "n"
    OPTION_BACK = "!"

    REF_VERSION = "version"
    REF_VERIFIER = "verifier"
    REF_CURR_OBJ = "curr_obj"

    ERR_SQLITE_CONSTRAINT_UNIQUE = "SQLITE_CONSTRAINT_UNIQUE"
    ERR_SQLITE_NO_DATA_FOUND = "NO_DATA_FOUND"

    COLOR_CLI_MESSAGE = "\033[93m"
    COLOR_CLI_LIST = "\033[96m"
    COLOR_CLI_INPUT = "\033[92m"
    COLOR_CLI_END = "\033[0m"
    BULLET_CLI_LIST = "\u2022"
    INTEND_CLI_LIST = 4
