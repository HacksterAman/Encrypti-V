from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

# Specify the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# Derive key from password
def deriveKeyFromPassword(password):
    # You can use a key derivation function (KDF) like PBKDF2 or Scrypt here
    # For simplicity, we'll use a basic hashing function
    hashed_password = hashlib.sha256(password.encode()).digest()
    return hashed_password

# Endpoint for encrypting files
@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files or 'key' not in request.form:
        return jsonify({'error': 'No file or key part'})

    file = request.files['file']
    key = request.form['key']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Derive key from the provided password
    key = deriveKeyFromPassword(key)

    # Read the file content
    file_bytes = file.read()

    # Encrypt the file content
    encrypted_bytes, iv = encryptBytes(file_bytes, key)

    # Save the encrypted file
    encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + file.filename)
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_bytes)

    return send_file(encrypted_file_path, as_attachment=True)


# Endpoint for decrypting files
@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files or 'key' not in request.form:
        return jsonify({'error': 'No file or key part'})

    file = request.files['file']
    key = request.form['key']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Derive key from the provided password
    key = deriveKeyFromPassword(key)

    # Read the file content
    file_bytes = file.read()

    # Extract IV and encrypted bytes
    iv = file_bytes[:16]  # IV size for AES-GCM is 16 bytes
    encrypted_bytes = file_bytes[16:]

    # Decrypt the file content
    decrypted_bytes = decryptBytes(encrypted_bytes, key, iv)

    if decrypted_bytes is not None:
        # Save the decrypted file
        decrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename[10:])
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_bytes)
        
        return send_file(decrypted_file_path, as_attachment=True)

    else:
        return jsonify({'error': 'Error decrypting file'})

if __name__ == '__main__':
    app.run(debug=True)
