# Dragon Vault

## About

A python module to store text documents as notes and other files in completely encrypted form that is accessible only through the module using the given password.

## Installation

Run the below command

```
pip install dvault
```

## Usage

Create a directory called Vault in your home directory (`C:\Users\<username>` for Windows and `/home/<username>` for Linux) and run the below command.

```
py -m dvault
```

Follow the on-screen instructions to create, view and delete notes and files in the Vault.

## Warnings

- Do not touch the files created inside Vault directory as they are sensitive to even minor changes and might lead to permanent data loss.

- The password entered is the only way to retrieve the data saved and loss of password leads to permanent data loss. There is no limit to the number of attempts so you can take your time to retrieve the password.

- Since this is a script based tool, it is vunerable to attacks where the script of the application is tampered and the password gets logged somewhere.
