# Encrypti V - Secure File Encryption and Decryption Tool

![Encrypti V Logo](logo.png)

Encrypti V is a file encryption and decryption tool that provides a secure way to protect your files. With Encrypti V, you can encrypt your sensitive files and decrypt them when needed. 
This README file will guide you through setting up the tool, configuring the database, and listing the required Python modules.

## Table of Contents

- [Introduction](#encrypti-v---secure-file-encryption-and-decryption-tool)
- [Features](#features)
- [Setup](#setup)
  - [Database Configuration](#database-configuration)
  - [Required Modules](#required-modules)
- [How to Use](#how-to-use)
- [Acknowledgements](#acknowledgements)

## Features

- User registration and login
- Secure file encryption using AES-GCM
- File decryption with the correct encryption key
- Option to change the file name during encryption
- Option to save encrypted files in a different location
- Strong password enforcement
- Secure storage of encryption keys in a database

## Setup

To set up Encrypti V, follow these steps:

### Database Configuration

1. Make sure you have a MySQL database server set up and running.
2. Create a database named `encryptiv_db` in your MySQL server.
3. Update the database connection details in the `Encrypti_V.py` script.

```python
connection = pymysql.connect(host="localhost", user="your_username", password="your_password", database="encryptiv_db")
```

### Required Modules

You need to install the following Python modules using `pip`:

- `pymysql`
- `Crypto`

You can install these modules by running the following commands:

```bash
pip install pymysql
pip install pycryptodome
```

## How to Use

1. Run the `Encrypti_V.py` script using Python.(Location: Encrypti V\src\Encrypti_V.py)

```bash
python Encrypti_V.py
```

2. You will be prompted to log in or register as a user.

3. After logging in, you can use the following options:
   - **Encrypt**: Select a file to encrypt, choose encryption options, and save the encrypted file.
   - **Decrypt**: Select an encrypted file, and it will be decrypted if you have the correct encryption key.

4. Make sure to remember your username and password, as they are used for login.

## Acknowledgements

- This project was developed using the Python programming language and the [Tkinter](https://docs.python.org/3/library/tkinter.html) library for the graphical user interface.
- Encryption is performed using the [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) library, which provides a robust implementation of AES-GCM encryption.
