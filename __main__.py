import base64
import os
import sys

from . import Fernet
from . import InvalidToken
from . import Scrypt

from . import Constants
from . import Messages

from . import operations

vault_dir = f"{os.getenv("USERPROFILE")}{Constants.SLASH}Vault"

# checking if vault is present
if not os.path.isdir(vault_dir):
    print(Messages.VAULT_NOT_PRESENT)
    sys.exit(0)

vault_verifier_file = f"{vault_dir}{Constants.SLASH}verifier"
vault_notes = list(
    filter(
        lambda file_name: file_name.endswith(Constants.FILE_FORMAT_NOTE)
        and os.path.isfile(f"{vault_dir}{Constants.SLASH}{file_name}"),
        os.listdir(vault_dir),
    )
)
vault_files = list(
    filter(
        lambda file_name: file_name.endswith(Constants.FILE_FORMAT_FILE)
        and os.path.isfile(f"{vault_dir}{Constants.SLASH}{file_name}"),
        os.listdir(vault_dir),
    )
)

password_verified = False

if not os.path.isfile(vault_verifier_file):
    if len(vault_notes) + len(vault_files) > 0:
        print(Messages.VAULT_NOT_EMPTY)
        sys.exit(0)
    else:
        print(Messages.INITIALIZING_VAULT)
        kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)

        password = input(Messages.ENTER_PASSWORD)
        fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

        with open(vault_verifier_file, "wb") as verifier_file:
            verifier_file.write(
                base64.urlsafe_b64decode(
                    fernet.encrypt(
                        "success".encode()
                    )
                )
            )
        print(Messages.VAULT_INITIALIZED)

        # no need to take password again
        password_verified = True

if not password_verified:
    kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)

    password = input(Messages.ENTER_PASSWORD)
    fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    with open(vault_verifier_file, "rb") as verifier_file:
        try:
            verifier_file_decrypted = fernet.decrypt(
                base64.urlsafe_b64encode(
                    verifier_file.read()
                )
            ).decode()
            if verifier_file_decrypted == "success":

                # clearing screen to prevent password peeping
                os.system(Constants.CLEAR_COMMAND)
            else:
                raise InvalidToken
        except InvalidToken:
            print(Messages.PASSWORD_VERIFICATION_FAILURE)
            sys.exit(0)

# welcome prompt
print(Messages.WELCOME)

while True:
    option = input(Messages.NOTES_OR_FILES)
    if option == "!":
        print(Messages.EXIT_VAULT)
        break
    elif option in ("n", "f"):
        menu_name = option
        while menu_name != "":
            if option == "n":
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=vault_dir, files=vault_notes
                )
            else:
                menu_name = operations.execute(
                    menu_name, fernet=fernet, vault_dir=vault_dir, files=vault_files
                )
    else:
        print(Messages.INVALID_OPTION)
