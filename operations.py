import os

from . import Constants
from . import DBEngine
from . import Messages
from . import Utils
from . import VaultCore


class Operations:
    def __init__(self, vault_core: VaultCore, db_engine: DBEngine):
        self.vault_core = vault_core
        self.db_engine = db_engine

    def execute(self, option: str):
        entry_type = None
        method_to_use = None
        match option:
            case "n":
                entry_type = "Notes"
                method_to_use = self.db_engine.get_notes
            case "f":
                entry_type = "Files"
                method_to_use = self.db_engine.get_files
            case _:
                Utils.print("Invalid option")
                return

        while True:
            list_of_entries = {
                id: self.vault_core.decrypt_string(enc_name)
                for id, enc_name in method_to_use()
            }
            Utils.print(f"{entry_type} present in the vault :")
            Utils.print_list(list(list_of_entries.values()))

            option = Utils.input("Do you want to read/write or delete (r, w, d) : ")
            match option:
                case "r":
                    try:
                        self.execute_r(entry_type)
                    except Exception as e:
                        if e.args[0] == "NO_DATA_FOUND":
                            Utils.print("Entry does not exist")
                        else:
                            raise
                case "w":
                    try:
                        self.execute_w(entry_type)
                    except Exception as e:
                        if e.args[0] == "SQLITE_CONSTRAINT_UNIQUE":
                            Utils.print("Entry already exists")
                        else:
                            raise
                case "d":
                    try:
                        self.execute_d(entry_type)
                    except Exception as e:
                        if e.args[0] == "NO_DATA_FOUND":
                            Utils.print("Entry does not exist")
                        else:
                            raise
                case "!":
                    break
                case _:
                    Utils.print("Invalid option")

    def execute_r(self, entry_type: str):
        entry_name = Utils.input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        if entry_type == "Notes":
            self.read_note(entry_name)
        else:
            self.read_file(entry_name)

    def execute_w(self, entry_type: str):
        entry_name = Utils.input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        entry_file = Utils.input(Messages.ENTER_FILE)
        if entry_file == "!":
            return
        if entry_type == "Notes":
            self.write_note(entry_name, entry_file)
        else:
            self.write_file(entry_name, entry_file)

    def execute_d(self, entry_type: str):
        entry_name = Utils.input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        if entry_type == "Notes":
            self.del_note(entry_name)
        else:
            self.del_file(entry_name)

    def read_note(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = self.db_engine.get_note_objects(enc_name)

        obj_array = b""
        for object in objects:
            with open(os.path.join(Constants.VAULT_DIR, object[1]), "rb") as obj_file:
                obj_array += obj_file.read()

        dec_obj_array = self.vault_core.decrypt_bytes(obj_array)
        Utils.print(dec_obj_array.decode(), is_colored=False)

    def write_note(self, entry_name: str, entry_file: str):
        obj_name = self.db_engine.get_reference("curr_obj")
        with open(entry_file, "r") as note_file:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "wb") as obj_file:
                obj_file.write(self.vault_core.encrypt_bytes(note_file.read().encode()))

        enc_name = self.vault_core.encrypt_string(entry_name)
        self.db_engine.insert_note_and_objects(enc_name, obj_name)
        self.db_engine.put_reference("curr_obj", Utils.get_next_object_name(obj_name))

    def del_note(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = self.db_engine.get_note_objects(enc_name)

        for object in objects:
            object_file = os.path.join(Constants.VAULT_DIR, object[1])
            if os.path.isfile(object_file):
                os.remove(object_file)
            self.db_engine.delete_object(object[0])

        self.db_engine.delete_note(enc_name)

    def read_file(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = self.db_engine.get_file_objects(enc_name)

        dest_file = Utils.input(Messages.ENTER_FILE)
        if dest_file == "!":
            return
        if os.path.isfile(dest_file):
            response = Utils.input(
                "File already exists, do you want to override (y, n) :"
            )
            if response == "!":
                return
            if response != "y":
                return

        obj_array = b""
        for object in objects:
            with open(os.path.join(Constants.VAULT_DIR, object[1]), "rb") as obj_file:
                obj_array += obj_file.read()

        dec_obj_array = self.vault_core.decrypt_bytes(obj_array)
        with open(dest_file, "wb") as data_file:
            data_file.write(dec_obj_array)

    def write_file(self, entry_name: str, entry_file: str):
        obj_name = self.db_engine.get_reference("curr_obj")
        with open(entry_file, "rb") as data_file:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "wb") as obj_file:
                obj_file.write(self.vault_core.encrypt_bytes(data_file.read()))

        enc_name = self.vault_core.encrypt_string(entry_name)
        self.db_engine.insert_file_and_objects(enc_name, obj_name)
        self.db_engine.put_reference("curr_obj", Utils.get_next_object_name(obj_name))

    def del_file(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = self.db_engine.get_file_objects(enc_name)

        for object in objects:
            object_file = os.path.join(Constants.VAULT_DIR, object[1])
            if os.path.isfile(object_file):
                os.remove(object_file)
            self.db_engine.delete_object(object[0])

        self.db_engine.delete_file(enc_name)
