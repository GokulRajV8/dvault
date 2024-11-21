import os


class Constants:
    MY_BIRTH_DAY_UNIX_SECONDS = 860201400
    MY_BIRTH_DAY_BYTE_ARRAY = b"05 April 1997 AD"
    SALT = b"\x18\xec7$\xd9\x85\xc87$i\xa3\xfeZ-\xd49\xe2\xb1$\x11\xc3C\xe5\xf1\xc0\xf8\x136%\xd7\xcd!"
    VAULT_DIR = os.path.join(os.getenv("USERPROFILE"), "Vault")
    VAULT_DB_FILE = os.path.join(VAULT_DIR, "master.db")
