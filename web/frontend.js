const fileInput = document.getElementById('fileInput');
const passwordInput = document.getElementById('passwordInput');
const formData = new FormData();

function deriveKeyFromPassword(password) {
    // You can use a key derivation function (KDF) like PBKDF2 or Scrypt here
    // For simplicity, we'll use a basic hashing function
    const encoder = new TextEncoder();
    return crypto.subtle.digest('SHA-256', encoder.encode(password));
}

async function encryptFile() {
    const password = passwordInput.value;

    // Derive key from password
    const key = await deriveKeyFromPassword(password);

    formData.append('file', fileInput.files[0]);
    formData.append('key', key);
    let filename = ""

    fetch('http://localhost:5000/encrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        filename = response.headers.get('Content-Disposition').split('filename=')[1].slice(1,-1);
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; // Change the filename as needed
        // a.download = "filename";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function decryptFile() {
    const password = passwordInput.value;

    // Derive key from password
    const key = await deriveKeyFromPassword(password);

    formData.append('file', fileInput.files[0]);
    formData.append('key', key);
    let filename = ""
    fetch('http://localhost:5000/decrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        filename = response.headers.get('Content-Disposition').split('filename=')[1].slice(1,-1);
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; // Change the filename as needed
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
