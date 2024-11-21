from . import Constants


class Messages:
    VAULT_NOT_PRESENT = "Vault directory is not present at your home directory\nKindly create ~/Vault directory before starting me"
    INITIALIZING_VAULT = "Vault is empty, initializing new vault ..."
    ENTER_PASSWORD = f"{Constants.COLOR_CLI_INPUT}Enter the password for vault : {Constants.COLOR_CLI_END}"
    PASSWORD_VERIFICATION_SUCCESS = "Password verification success"
    PASSWORD_VERIFICATION_FAILURE = "Password verification failed"
    DB_FATAL_ERROR = "Fatal error occurred while accessing database, most likely due to corruption.\nKindly delete all files present in ~/Vault as they are tampered"
    DEC_FATAL_ERROR = "Fatal error occurred while decrypting data"
    WELCOME = f"Welcome to your personal Vault\nEnter {Constants.OPTION_BACK} to go back at any point"
    EXIT = "Thank you for using Vault"
    ENTER_NOTES_OR_FILES = f"Do you want to process notes or files ({Constants.OPTION_NOTES}, {Constants.OPTION_FILES}) : "
    ENTER_OPERATION = f"Do you want to read/write or delete ({Constants.OPTION_READ}, {Constants.OPTION_WRITE}, {Constants.OPTION_DELETE}) : "
    ENTER_NAME = "Enter name : "
    ENTER_LOCATION = "Enter location : "
    INVALID_OPTION = "Invalid option"
    ENTRY_DOES_NOT_EXIST = "Entry does not exist"
    ENTRY_ALREADY_EXISTS = "Entry already exists"
    ENTER_OVERRIDE_FILE = f"File already exists, do you want to override ({Constants.OPTION_YES}, {Constants.OPTION_NO}) : "
    FILE_DOES_NOT_EXIST = "File does not exist"
