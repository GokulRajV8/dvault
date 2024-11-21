class Messages:
    VAULT_NOT_PRESENT = "Vault directory is not present at your home directory\nKindly create ~/Vault directory before starting me"
    INITIALIZING_VAULT = "Vault is empty, initializing new vault ..."
    ENTER_PASSWORD = "\033[92mEnter the password for vault : \033[0m"
    PASSWORD_VERIFICATION_SUCCESS = "Password verification success"
    PASSWORD_VERIFICATION_FAILURE = "Password verification failed"
    DB_FATAL_ERROR = "Fatal error occurred while accessing database, most likely due to corruption.\nKindly delete all files present in ~/Vault as they are tampered"
    DEC_FATAL_ERROR = "Fatal error occurred while decrypting data"
    WELCOME = "Welcome to your personal Vault\nEnter ! to go back at any point"
    EXIT = "Thank you for using Vault"

    ENTER_NAME = "Enter name : "
    ENTER_FILE = "Enter file location : "
