# 🔐 Codveda | File Encryption & Decryption

A professional desktop application for encrypting and decrypting files,
built with **Python**, **Tkinter**, and the **cryptography** library
(Fernet symmetric encryption). Developed as part of the Codveda internship
program.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## ✨ Features

- 🎨 Modern dark-themed graphical interface
- 📂 Browse and select any file from your system
- 🔒 Encrypt files using Fernet (AES 128 in CBC mode + HMAC)
- 🔓 Decrypt previously encrypted files back to their original form
- 🔑 Automatic secure key generation and storage (`key.key`)
- 💬 Clear success and error dialogs via `messagebox`
- 🧹 One-click clear/reset of the current selection
- 🖥️ Automatically centered window on launch

---

## 🖼️ Application Overview

| Button          | Action                                              |
|------------------|------------------------------------------------------|
| **Browse File**  | Opens a file dialog to select a file                 |
| **Encrypt**      | Encrypts the selected file and saves the output       |
| **Decrypt**      | Decrypts a previously encrypted file                  |
| **Clear**        | Clears the current file selection                     |
| **Exit**         | Closes the application                                 |

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/codveda-file-encryptor.git
cd codveda-file-encryptor
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Tkinter ships with most standard Python installations. If it's
> missing on Linux, install it via your package manager, e.g.
> `sudo apt-get install python3-tk`.

---

## 🚀 Usage

Run the application:

```bash
python file_encryptor.py
```

1. Click **Browse File** to select the file you want to encrypt or decrypt.
2. Click **Encrypt** to generate an encrypted copy of the file (a key is
   generated automatically the first time and stored in `key.key`).
3. Click **Decrypt** to restore an encrypted file to its original content
   (requires the same `key.key` used to encrypt it).
4. Use **Clear** to reset your selection, or **Exit** to close the app.

---

## 🔑 About the Encryption Key

- The app uses **Fernet** symmetric encryption from the `cryptography`
  library, which is built on AES-128 in CBC mode with HMAC for integrity.
- On first use, a key is generated and saved to `key.key` in the project
  directory.
- **Keep `key.key` safe and private.** Anyone with this file can decrypt
  your files, and losing it means encrypted files can never be recovered.
- `key.key` is excluded from version control via `.gitignore` to prevent
  accidental exposure.

---

## 📁 Project Structure

```
codveda-file-encryptor/
├── file_encryptor.py   # Main application (GUI + encryption logic)
├── README.md            # Project documentation
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
└── .gitignore             # Files/folders excluded from Git
```

---

## 🧰 Built With

- [Python 3](https://www.python.org/) — Core language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework
- [cryptography](https://cryptography.io/) — Fernet symmetric encryption

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE)
file for details.

---

## 🙋 Author

Developed as part of the **Codveda Internship Program**.
