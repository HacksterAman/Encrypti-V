# Encrypti V - Secure File Encryption and Decryption Tool

Encrypti V is a file encryption and decryption tool designed to provide a secure way to protect your files. 
This README provides instructions on setting up the tool, configuring the database, and listing the required modules for both the Python and Java versions.

## Table of Contents

- [Introduction](#encrypti-v---secure-file-encryption-and-decryption-tool)
- [Features](#features)
- [Python Version](#python-version)
  - [Setup](#setup)
  - [Required Modules](#required-modules)
- [Java Version](#java-version)
  - [Setup](#java-setup)
  - [Required Libraries](#required-libraries)
- [How to Use](#how-to-use)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features

- User registration and login
- Secure file encryption using AES-GCM
- File decryption with the correct encryption key
- Option to change the file name during encryption
- Option to save encrypted files in a different location
- Strong password enforcement
- Secure storage of encryption keys in a database

## Python Version

### Setup

To set up the Python version of Encrypti V, follow these steps:

#### Database Configuration

1. Make sure you have a MySQL database server set up and running.
2. Create a database named `encryptiv_db` in your MySQL server.
3. Update the database connection details in the `Encrypti_V.py` script.

```python
connection = pymysql.connect(host="localhost", user="your_username", password="your_password", database="encryptiv_db")
```

#### Required Modules

You need to install the following Python modules using `pip`:

- `pymysql`
- `Crypto`

You can install these modules by running the following commands:

```bash
pip install pymysql
pip install pycryptodome
```

### How to Use

1. Run the `Encrypti_V.py` script using Python.

```bash
python Encrypti_V.py
```

2. You will be prompted to log in or register as a user.

3. After logging in, you can use the following options:

   - **Encrypt**: Select a file to encrypt, choose encryption options, and save the encrypted file.

   - **Decrypt**: Select an encrypted file, and it will be decrypted if you have the correct encryption key.

4. Make sure to remember your username and password, as they are used for login.

## Java Version

### Setup

To set up the Java version of Encrypti V, follow these steps:

#### Database Configuration

1. Make sure you have a MySQL database server set up and running.
2. Create a database named `encryptiv_db` in your MySQL server.
3. Update the database connection details in the `Encrypti_V.java` script.

```java
String jdbcUrl = "jdbc:mysql://localhost:3306/encryptiv_db";
String username = "your_username";
String password = "your_password";
```

#### Required Libraries

You need to include the following Java libraries:

- `javax.crypto`
- `javax.swing`
- `java.awt`
- `java.io`
- `java.nio.file`
- `java.security`
- `java.sql`
- `java.util`

### How to Use

1. Compile and run the `Encrypti_V.java` script.

```bash
javac Encrypti_V.java
java Encrypti_V
```

2. You will be prompted to log in or register as a user.

3. After logging in, you can use the following options:

   - **Encrypt**: Select a file to encrypt, choose encryption options, and save the encrypted file.

   - **Decrypt**: Select an encrypted file, and it will be decrypted if you have the correct encryption key.

4. Make sure to remember your username and password, as they are used for login.

## Acknowledgements

- This project was developed using the Python programming language for the Python version and Java for the Java version.

- Encryption is performed using the Python version with the [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) library and the Java version using Java's built-in encryption capabilities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
