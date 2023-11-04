from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import random
import string
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import pymysql

# Function to establish a database connection
def connectToDatabase():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="AmanSingh197@", database="encryptiv_db")
        return connection
    except Exception as e:
        print(e)
        return None

# Function to display a message dialog
def showMessage(message):
    messagebox.showinfo("Message", message)

# Function to register a user
def register(connection, username, password):
    if username is None or password is None:
        showMessage("Enter a Valid Username and password.")
    elif isStrongPassword(password):
        try:
            with connection.cursor() as cursor:
                insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (username, hashPassword(password)))
            connection.commit()
            return True
        except Exception as e:
            print(e)
    else:
        showMessage("Enter a Strong password.")
    return False

# Function to perform user login
def login(connection, username, password):
    try:
        with connection.cursor() as cursor:
            query = "SELECT user_id FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashPassword(password)))
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as e:
        print(e)
    return -1

# Function to check if a password is strong
def isStrongPassword(password):
    return password is not None and re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[_@#$%^&+=!]).{8,}$", password)

# Function to hash a password
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check the entered password against a hashed password
def checkPassword(enteredPassword, hashedPassword):
    return hashPassword(enteredPassword) == hashedPassword

# Function to open a file picker dialog
def pickFile():
    return filedialog.askopenfilename()

# Function to open a directory picker dialog
def pickDir():
    return filedialog.askdirectory()

# Function to store encryption keys in the database
def storeKeyInDatabase(connection, userId, fileId, fileName, keyBytes, iv):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO files (user_id, file_id, file_name, encryption_key, iv) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (userId, fileId, fileName, keyBytes, iv))
        connection.commit()
    except Exception as e:
        print(e)

# Function to perform file encryption
def performEncryption(selectedFile, encryptDialog, createNewName, saveInNewLocation):
    encryptDialog.destroy()
    try:
        selectedDir = os.path.dirname(selectedFile) if not saveInNewLocation else pickDir()
        originalFileName = os.path.basename(selectedFile)
        fileId = generateRandomKey()
        fileName = os.path.splitext(originalFileName)[0] if not createNewName else generateRandomFileName()
        keyBytes = generateRandomKey()
        with open(selectedFile, "rb") as file:
            fileBytes = file.read()
        encryptedFileBytes, iv = encryptBytes(fileBytes, keyBytes)
        cipher = fileId + encryptedFileBytes
        storeKeyInDatabase(connection, userId, fileId, originalFileName, keyBytes, iv)
        with open(os.path.join(selectedDir, fileName + ".V"), "wb") as file:
            file.write(cipher)
        os.remove(selectedFile)
        showMessage("File encrypted successfully.")
    except Exception as e:
        print(e)
        showMessage("Error encrypting file.")

# Function to initiate the file encryption process
def encryptFile():
    selectedFile = pickFile()
    if selectedFile is None:
        return
    encryptDialog = Toplevel(root)
    encryptDialog.title("Encryption Options")
    encryptDialog.geometry("300x150")

    createNewName = BooleanVar()
    saveInNewLocation = BooleanVar()

    createNewNameCheckBox = Checkbutton(encryptDialog, text="Change File Name", variable=createNewName)
    saveInNewLocationCheckBox = Checkbutton(encryptDialog, text="Save in New Location", variable=saveInNewLocation)

    encryptButton = Button(encryptDialog, text="Encrypt", command=lambda: performEncryption(selectedFile, encryptDialog, createNewName.get(), saveInNewLocation.get()))
    cancelButton = Button(encryptDialog, text="Cancel", command=encryptDialog.destroy)

    createNewNameCheckBox.pack()
    saveInNewLocationCheckBox.pack()
    encryptButton.pack()
    cancelButton.pack()

# Function to retrieve file details from the database
def fileDetails(connection, fileId):
    try:
        with connection.cursor() as cursor:
            query = "SELECT file_name, encryption_key, iv FROM files WHERE file_id = %s AND user_id = %s"
            cursor.execute(query, (fileId, userId))
            result = cursor.fetchone()
            if result:
                return result
    except Exception as e:
        print(e)
    return None

# Function to delete a database record
def deleteRecord(connection, fileId):
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM files WHERE file_id = %s AND user_id = %s"
            cursor.execute(query, (fileId, userId))
        connection.commit()
    except Exception as e:
        print(e)

# Function to perform file decryption
def decryptFile():
    selectedFile = pickFile()
    if selectedFile is None:
        return
    try:
        with open(selectedFile, "rb") as file:
            cipher = file.read()
        fileId = cipher[:32]
        encryptedFileBytes = cipher[32:]
        details = fileDetails(connection, fileId)
        originalFileName = details[0]
        keyBytes = details[1]
        iv = details[2]
        decryptedBytes = decryptBytes(encryptedFileBytes, keyBytes, iv)
        if decryptedBytes is not None:
            originalDir = os.path.dirname(selectedFile)
            decryptedFile = os.path.join(originalDir, originalFileName)
            with open(decryptedFile, "wb") as file:
                file.write(decryptedBytes)
            os.remove(selectedFile)
            deleteRecord(connection, fileId)
            showMessage("File decrypted successfully and saved as " + os.path.basename(decryptedFile))
        else:
            showMessage("Error decrypting file. Please make sure you selected the correct encryption key.")
    except Exception as e:
        print(e)
        showMessage("Error decrypting file.")

# Function to generate a random encryption key
def generateRandomKey():
    return get_random_bytes(32)

# Function to encrypt bytes using AES-GCM
def encryptBytes(bytes, key):
    cipher = AES.new(key, AES.MODE_GCM)
    encryptedBytes, tag = cipher.encrypt_and_digest(pad(bytes, AES.block_size))
    return encryptedBytes, cipher.nonce

# Function to decrypt bytes using AES-GCM
def decryptBytes(encryptedText, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    try:
        decryptedBytes = unpad(cipher.decrypt(encryptedText), AES.block_size)
        return decryptedBytes
    except (ValueError, KeyError):
        return None

# Function to generate a random file name
def generateRandomFileName():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to hide components
def hideComponents(*components):
    for component in components:
        component.place_forget()

# Function to show encryption and decryption buttons
def showButtons():
    encryptFileButton.place(x=100, y=110, width=90, height=30)
    decryptFileButton.place(x=210, y=110, width=90, height=30)

# Function to handle login button click
def loginButtonClicked(username, password):
    global userId
    userId = login(connection, username, password)
    if userId == -1:
        showMessage("Login failed. Invalid username or password.")
    else:
        hideComponents(usernameLabel, usernameField, passwordField, passwordLabel, loginButton, registerButton)
        showButtons()

# Function to handle register button click
def registerButtonClicked(username, password):
    if register(connection, username, password):
        showMessage("Registration successful. You can now log in")

# Create the main Tkinter window
root = Tk()
root.geometry("400x250")
root.title("Encrypti V")
root.resizable(False, False)

# Load the background image
backgroundImage = PhotoImage(file="C:\\Users\\amams\\OneDrive\\Desktop\\Codes\\Encrypti V\\src\\background.gif")
backgroundLabel = Label(root, image=backgroundImage)
backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

# Initialize user ID and establish a database connection
userId = 0
connection = connectToDatabase()

if connection is None:
    showMessage("Connection failed. Try again later.")
    sys.exit(1)

# Create and place UI elements
usernameLabel = Label(root, text="Username:")
usernameLabel.place(x=50, y=80)
passwordLabel = Label(root, text="Password:")
passwordLabel.place(x=50, y=120)
usernameField = Entry(root)
usernameField.place(x=140, y=80, width=200, height=25)
passwordField = Entry(root, show="*")
passwordField.place(x=140, y=120, width=200, height=25)
loginButton = Button(root, text="Login", command=lambda: loginButtonClicked(usernameField.get(), passwordField.get()))
loginButton.place(x=140, y=160, width=90, height=30)
registerButton = Button(root, text="Register", command=lambda: registerButtonClicked(usernameField.get(), passwordField.get()))
registerButton.place(x=250, y=160, width=90, height=30)
encryptFileButton = Button(root, text="Encrypt", command=encryptFile)
decryptFileButton = Button(root, text="Decrypt", command=decryptFile)

hideComponents(encryptFileButton, decryptFileButton)

root.mainloop()
