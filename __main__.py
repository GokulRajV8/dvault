import getpass
import os

from . import Constants
from . import DBEngine
from . import Messages
from . import Operations
from . import Utils
from . import VaultCore


def create_empty_db() -> bool:
    if not (
        os.path.isfile(Constants.VAULT_DB_FILE)
        and os.path.getsize(Constants.VAULT_DB_FILE) != 0
    ):
        Utils.print(Messages.INITIALIZING_VAULT)
        open(Constants.VAULT_DB_FILE, "w").close()
        return True
    else:
        return False


def init_db(db_engine: DBEngine, verifier_string: str):
    db_engine.create_tables()
    db_engine.put_reference(Constants.REF_VERSION, Constants.APP_VERSION)
    db_engine.put_reference(Constants.REF_VERIFIER, verifier_string)
    db_engine.put_reference(Constants.REF_CURR_OBJ, Utils.get_next_object_name())


def verify_password(db_engine: DBEngine, verifier_string: str):
    verifier_string_from_db = db_engine.get_reference(Constants.REF_VERIFIER)
    if verifier_string_from_db == verifier_string:
        Utils.print(Messages.PASSWORD_VERIFICATION_SUCCESS)
    else:
        raise ValueError(Messages.PASSWORD_VERIFICATION_FAILURE)


def menu_loop(vault_core: VaultCore, db_engine: DBEngine):
    operations_module = Operations(vault_core, db_engine)
    while True:
        option = Utils.input(Messages.ENTER_NOTES_OR_FILES)
        if option == Constants.OPTION_BACK:
            break
        else:
            operations_module.execute(option)


if __name__ == "__main__":
    db_engine = None
    try:
        # checking for presence of vault
        if not os.path.isdir(Constants.VAULT_DIR):
            raise FileNotFoundError(Messages.VAULT_NOT_PRESENT)

        # if the database is not present or empty, create a new one
        is_new_vault = create_empty_db()

        # take password from user and generate vault core for encryption and decryption
        vault_core = VaultCore(getpass.getpass(Messages.ENTER_PASSWORD))
        verifier_string = vault_core.encrypt_string(Constants.VERIFIER_STRING)

        # creating database engine
        db_engine = DBEngine(Constants.VAULT_DB_FILE)

        # if new vault, create relevant tables in database and insert data
        # else, verify the entered password
        if is_new_vault:
            init_db(db_engine, verifier_string)
        else:
            verify_password(db_engine, verifier_string)

        # welcome prompt and menu loop
        Utils.print(Messages.WELCOME)
        menu_loop(vault_core, db_engine)

        # exit prompt
        Utils.print(Messages.EXIT)

    except Exception as e:
        Utils.print(e.args[0])

    finally:
        # closing the db engine
        if db_engine:
            db_engine.close()
