import os

from . import Constants
from . import DBEngine
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
                entry_type = Constants.ENTRY_TYPE_NOTES
                method_to_use = self.db_engine.get_notes
            case "f":
                entry_type = Constants.ENTRY_TYPE_FILES
                method_to_use = self.db_engine.get_files
            case _:
                Utils.print("Invalid option")
                return

        while True:
            list_of_entries = {
                id: self.vault_core.decrypt_string(enc_name)
                for id, enc_name in method_to_use()
            }
            Utils.print(entry_type + " present in the vault :")
            Utils.print_list(list(list_of_entries.values()))

            option = Utils.input("Do you want to read/write or delete (r, w, d) : ")
            entry_name = Utils.input("Enter name : ")
            try:
                match option:
                    case "r":
                        self.execute_r(entry_type, entry_name)
                    case "w":
                        self.execute_w(entry_type, entry_name)
                    case "d":
                        self.execute_d(entry_type, entry_name)
                    case Constants.OPTION_BACK:
                        break
                    case _:
                        Utils.print("Invalid option")
            except Exception as e:
                if e.args[0] == Constants.ERR_SQLITE_NO_DATA_FOUND:
                    Utils.print("Entry does not exist")
                elif e.args[0] == Constants.ERR_SQLITE_CONSTRAINT_UNIQUE:
                    Utils.print("Entry already exists")
                else:
                    raise

    def execute_r(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
            self.read_note(entry_name)
        else:
            self.read_file(entry_name)

    def execute_w(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        entry_location = Utils.input("Enter location : ")
        if entry_location == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
            self.write_note(entry_name, entry_location)
        else:
            self.write_file(entry_name, entry_location)

    def execute_d(self, message: str, entry_name: str):
        if entry_name == Constants.OPTION_BACK:
            return
        if message == Constants.ENTRY_TYPE_NOTES:
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
        print(dec_obj_array.decode())

    def write_note(self, entry_name: str, entry_location: str):
        if not os.path.isfile(os.path.join(entry_location, entry_name)):
            Utils.print("File does not exist")
            return

        obj_name = self.db_engine.get_reference(Constants.CURR_OBJ)
        with open(os.path.join(entry_location, entry_name), "r") as note_file:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "wb") as obj_file:
                obj_file.write(self.vault_core.encrypt_bytes(note_file.read().encode()))

        enc_name = self.vault_core.encrypt_string(entry_name)
        self.db_engine.insert_note_and_objects(enc_name, obj_name)
        self.db_engine.put_reference(
            Constants.CURR_OBJ, Utils.get_next_object_name(obj_name)
        )

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

        dest_location = Utils.input("Enter location : ")
        if dest_location == Constants.OPTION_BACK:
            return
        if os.path.isfile(os.path.join(dest_location, entry_name)):
            response = Utils.input(
                "File already exists, do you want to override (y, n) : "
            )
            if response in [Constants.OPTION_BACK, Constants.OPTION_NO]:
                return

        obj_array = b""
        for object in objects:
            with open(os.path.join(Constants.VAULT_DIR, object[1]), "rb") as obj_file:
                obj_array += obj_file.read()

        dec_obj_array = self.vault_core.decrypt_bytes(obj_array)
        with open(os.path.join(dest_location, entry_name), "wb") as data_file:
            data_file.write(dec_obj_array)

    def write_file(self, entry_name: str, entry_location: str):
        if not os.path.isfile(os.path.join(entry_location, entry_name)):
            Utils.print("File does not exist")
            return

        obj_name = self.db_engine.get_reference(Constants.CURR_OBJ)
        with open(os.path.join(entry_location, entry_name), "rb") as data_file:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "wb") as obj_file:
                obj_file.write(self.vault_core.encrypt_bytes(data_file.read()))

        enc_name = self.vault_core.encrypt_string(entry_name)
        self.db_engine.insert_file_and_objects(enc_name, obj_name)
        self.db_engine.put_reference(
            Constants.CURR_OBJ, Utils.get_next_object_name(obj_name)
        )

    def del_file(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        objects = self.db_engine.get_file_objects(enc_name)

        for object in objects:
            object_file = os.path.join(Constants.VAULT_DIR, object[1])
            if os.path.isfile(object_file):
                os.remove(object_file)
            self.db_engine.delete_object(object[0])

        self.db_engine.delete_file(enc_name)
