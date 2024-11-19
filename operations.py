import os

from . import Constants
from . import DBEngine
from . import Messages
from . import Queries
from . import Utils
from . import VaultCore


class OperationsModule:
    def __init__(self, vault_core: VaultCore, db_engine: DBEngine):
        self.vault_core = vault_core
        self.db_engine = db_engine

    def execute(self, option: str):
        entry_type = None
        query_to_use = None
        match option:
            case "n":
                entry_type = "Notes"
                query_to_use = Queries.GET_NOTES
            case "f":
                entry_type = "Files"
                query_to_use = Queries.GET_FILES
            case _:
                print("Invalid option")
                return

        while True:
            list_of_entries = {
                id: self.vault_core.decrypt_string(name_enc)
                for id, name_enc in self.db_engine.execute(query_to_use).fetchall()
            }
            print(f"{entry_type} present in the vault :")
            [print("    - " + entry) for entry in list(list_of_entries.values())]

            option = input("Do you want to read/write or delete (r, w, d) : ")
            match option:
                case "r":
                    self.execute_r(entry_type)
                case "w":
                    try:
                        self.execute_w(entry_type)
                    except Exception as e:
                        if e.args[0] == "SQLITE_CONSTRAINT_UNIQUE":
                            print("Entry already exists")
                        else:
                            raise
                case "d":
                    self.execute_d(entry_type)
                case "!":
                    break
                case _:
                    print("Invalid option")

    def execute_r(self, entry_type: str):
        entry_name = input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        if entry_type == "Notes":
            self.read_note(entry_name)
        else:
            self.read_file(entry_name)

    def execute_w(self, entry_type: str):
        entry_name = input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        entry_file = input(Messages.ENTER_FILE)
        if entry_file == "!":
            return
        if entry_type == "Notes":
            self.write_note(entry_name, entry_file)
        else:
            self.write_file(entry_name, entry_file)

    def execute_d(self, entry_type: str):
        entry_name = input(Messages.ENTER_NAME)
        if entry_name == "!":
            return
        if entry_type == "Notes":
            self.del_note(entry_name)
        else:
            self.del_file(entry_name)

    def read_note(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        file_id = self.db_engine.execute(Queries.GET_NOTE_ID, (enc_name,)).fetchone()[0]
        obj_names = [
            entry[2]
            for entry in self.db_engine.execute(
                Queries.GET_OBJECTS, (file_id,)
            ).fetchall()
        ]

        obj_array = b""
        for obj_name in obj_names:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "rb") as obj_file:
                obj_array += obj_file.read()

        dec_obj_array = self.vault_core.decrypt_bytes(obj_array)
        print(dec_obj_array.decode())

    def write_note(self, entry_name: str, entry_file: str):
        obj_name = self.db_engine.get_reference("curr_obj")
        with open(entry_file, "r") as note_file:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "wb") as obj_file:
                obj_file.write(self.vault_core.encrypt_bytes(note_file.read().encode()))

        enc_name = self.vault_core.encrypt_string(entry_name)
        self.db_engine.execute(Queries.INSERT_NOTE, (enc_name,))
        file_id = self.db_engine.execute(Queries.GET_NOTE_ID, (enc_name,)).fetchone()[0]
        self.db_engine.execute(Queries.INSERT_OBJECT, (file_id, 0, obj_name))
        self.db_engine.put_reference("curr_obj", Utils.get_next_object_name(obj_name))

    def del_note(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        file_id = self.db_engine.execute(Queries.GET_NOTE_ID, (enc_name,)).fetchone()[0]
        objects = [
            (entry[0], entry[2])
            for entry in self.db_engine.execute(
                Queries.GET_OBJECTS, (file_id,)
            ).fetchall()
        ]

        for object in objects:
            object_file = os.path.join(Constants.VAULT_DIR, object[1])
            if os.path.isfile(object_file):
                os.remove(object_file)
            self.db_engine.execute(Queries.DEL_OBJECT, (object[0],))

        self.db_engine.execute(Queries.DEL_FILE, (file_id,))

    def read_file(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        dest_file = input(Messages.ENTER_FILE)
        if dest_file == "!":
            return
        if os.path.isfile(dest_file):
            response = input("File already exists, do you want to override (y, n) :")
            if response == "!":
                return
            if response != "y":
                return

        file_id = self.db_engine.execute(Queries.GET_FILE_ID, (enc_name,)).fetchone()[0]
        obj_names = [
            entry[2]
            for entry in self.db_engine.execute(
                Queries.GET_OBJECTS, (file_id,)
            ).fetchall()
        ]

        obj_array = b""
        for obj_name in obj_names:
            with open(os.path.join(Constants.VAULT_DIR, obj_name), "rb") as obj_file:
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
        self.db_engine.execute(Queries.INSERT_FILE, (enc_name,))
        file_id = self.db_engine.execute(Queries.GET_FILE_ID, (enc_name,)).fetchone()[0]
        self.db_engine.execute(Queries.INSERT_OBJECT, (file_id, 0, obj_name))
        self.db_engine.put_reference("curr_obj", Utils.get_next_object_name(obj_name))

    def del_file(self, entry_name: str):
        enc_name = self.vault_core.encrypt_string(entry_name)
        file_id = self.db_engine.execute(Queries.GET_FILE_ID, (enc_name,)).fetchone()[0]
        objects = [
            (entry[0], entry[2])
            for entry in self.db_engine.execute(
                Queries.GET_OBJECTS, (file_id,)
            ).fetchall()
        ]

        for object in objects:
            object_file = os.path.join(Constants.VAULT_DIR, object[1])
            if os.path.isfile(object_file):
                os.remove(object_file)
            self.db_engine.execute(Queries.DEL_OBJECT, (object[0],))

        self.db_engine.execute(Queries.DEL_FILE, (file_id,))
