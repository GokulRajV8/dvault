"""
The operations are two levels deep and denoted by two characters.

First character denotes whether it is a note or file (n, f)
Second character denotes whether read, write or delete (r, w, d)
"""

import base64
import os

from . import Fernet

from . import Constants
from . import Messages


def execute(menu_name: str, **params) -> str:
    internal_local_scope = {}
    exec(
        f"menu = menu_{menu_name}",
        globals(),
        internal_local_scope,
    )
    menu = internal_local_scope["menu"]

    if menu_name in ("n", "f"):
        return menu(params["fernet"], params["files"])
    else:
        return menu(params["fernet"], params["vault_dir"], params["files"])


## Top level menus


def menu_n(fernet: Fernet, files: list[str]) -> str:
    print(Messages.NOTES_IN_VAULT)
    for file in files:
        decrypted_note_name = fernet.decrypt(file[:-8].encode()).decode()
        print(f"\t{decrypted_note_name}")

    option = input(Messages.READ_WRITE_OR_DELETE)
    if option == "!":
        return ""

    match option:
        case "r":
            return "nr"
        case "w":
            return "nw"
        case "d":
            return "nd"
        case _:
            print(Messages.INVALID_OPTION)
            return "n"


def menu_f(fernet: Fernet, files: list[str]) -> str:
    print(Messages.FILES_IN_VAULT)
    for file in files:
        decrypted_file_name = fernet.decrypt(file[:-8].encode()).decode()
        print(f"\t{decrypted_file_name}")

    option = input(Messages.READ_WRITE_OR_DELETE)
    if option == "!":
        return ""

    match option:
        case "r":
            return "fr"
        case "w":
            return "fw"
        case "d":
            return "fd"
        case _:
            print(Messages.INVALID_OPTION)
            return "f"


## Menus for notes


def menu_nr(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    note_file_name = input(Messages.ENTER_NOTE_NAME)
    if note_file_name == "!":
        return "n"

    note_file_name_enc = (
        fernet._encrypt_from_parts(
            note_file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_NOTE
    )

    if note_file_name_enc in files:
        with open(
            f"{vault_dir}{Constants.SLASH}{note_file_name_enc}", "rb"
        ) as file_to_be_read:
            file_content = fernet.decrypt(
                base64.urlsafe_b64encode(file_to_be_read.read())
            )
            print("Note content >>\n" + file_content.decode())
        return "n"
    else:
        print(Messages.NOTE_NOT_PRESENT)
        return "nr"


def menu_nw(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    note_file_name = input(Messages.ENTER_FILE_NAME)
    if note_file_name == "!":
        return "n"

    note_file_name_enc = (
        fernet._encrypt_from_parts(
            note_file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_NOTE
    )

    if note_file_name_enc in files:
        print(Messages.NOTE_ALREADY_PRESENT)
        return "nw"

    note_file_dir = input(Messages.ENTER_DIRECTORY_NAME)
    if note_file_dir == "!":
        return "n"

    if os.path.isfile(f"{note_file_dir}{Constants.SLASH}{note_file_name}"):
        with open(
            f"{note_file_dir}{Constants.SLASH}{note_file_name}", "rb"
        ) as file_to_be_read:
            with open(
                f"{vault_dir}{Constants.SLASH}{note_file_name_enc}", "wb"
            ) as file_to_be_written:
                file_to_be_written.write(
                    base64.urlsafe_b64decode(fernet.encrypt(file_to_be_read.read()))
                )
        print(Messages.NOTE_CREATED)
        return "n"
    else:
        print(Messages.FILE_NOT_PRESENT)
        return "nw"


def menu_nd(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    note_file_name = input(Messages.ENTER_NOTE_NAME)
    if note_file_name == "!":
        return "n"

    note_file_name_enc = (
        fernet._encrypt_from_parts(
            note_file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_NOTE
    )

    if note_file_name_enc in files:
        os.remove(f"{vault_dir}{Constants.SLASH}{note_file_name_enc}")
        print(Messages.NOTE_REMOVED)
        return "n"
    else:
        print(Messages.NOTE_NOT_PRESENT)
        return "nr"


## Menus for files


def menu_fr(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    file_name = input(Messages.ENTER_FILE_NAME)
    if file_name == "!":
        return "f"

    file_name_enc = (
        fernet._encrypt_from_parts(
            file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_FILE
    )

    if file_name_enc in files:
        dest_dir_name = input(Messages.ENTER_DIRECTORY_NAME)
        if dest_dir_name == "!":
            return "f"

        if os.path.isdir(dest_dir_name):
            dest_file = f"{dest_dir_name}{Constants.SLASH}{file_name}"

            if os.path.isfile(dest_file):
                print(Messages.FILE_ALREADY_PRESENT)
                return "fr"
            else:
                with open(
                    f"{vault_dir}{Constants.SLASH}{file_name_enc}", "rb"
                ) as file_to_be_read:
                    with open(dest_file, "wb") as file_to_be_written:
                        file_to_be_written.write(
                            fernet.decrypt(
                                base64.urlsafe_b64encode(file_to_be_read.read())
                            )
                        )
                    print(Messages.FILE_CREATED)
                    return "f"

        else:
            print(Messages.DIRECTORY_NOT_PRESENT)
            return "fr"
    else:
        print(Messages.FILE_NOT_PRESENT)
        return "fr"


def menu_fw(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    file_name = input(Messages.ENTER_FILE_NAME)
    if file_name == "!":
        return "f"

    file_name_enc = (
        fernet._encrypt_from_parts(
            file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_FILE
    )

    if file_name_enc in files:
        print(Messages.FILE_ALREADY_PRESENT)
        return "nw"

    file_dir = input(Messages.ENTER_DIRECTORY_NAME)
    if file_dir == "!":
        return "n"

    if os.path.isfile(f"{file_dir}{Constants.SLASH}{file_name}"):
        with open(f"{file_dir}{Constants.SLASH}{file_name}", "rb") as file_to_be_read:
            with open(
                f"{vault_dir}{Constants.SLASH}{file_name_enc}", "wb"
            ) as file_to_be_written:
                file_to_be_written.write(
                    base64.urlsafe_b64decode(fernet.encrypt(file_to_be_read.read()))
                )
        print(Messages.FILE_CREATED)
        return "f"
    else:
        print(Messages.FILE_NOT_PRESENT)
        return "fw"


def menu_fd(fernet: Fernet, vault_dir: str, files: list[str]) -> str:
    file_name = input(Messages.ENTER_FILE_NAME)
    if file_name == "!":
        return "f"

    file_name_enc = (
        fernet._encrypt_from_parts(
            file_name.encode(),
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        ).decode()
        + Constants.FILE_FORMAT_FILE
    )

    if file_name_enc in files:
        os.remove(f"{vault_dir}{Constants.SLASH}{file_name_enc}")
        print(Messages.FILE_REMOVED)
        return "n"
    else:
        print(Messages.FILE_NOT_PRESENT)
        return "nr"
