# Password-Manager

Building a secure password manager using Tkinter. The app includes both password generator and a password manager.


# security
The choice of making it an offline and a desktop-only app is for security mesures. That's why Tkinter was used in the project, and because the encryption key is stored locally, so it would take a long time to decrypt the master password without the key.

# Encryption

In this app, Fernet algorithm was used because it is based on the Advanced Encryption Standard (AES) in symmetric mode, which is a widely recognized and secure encryption algorithm. It ensures that passwords are protected from unauthorized access and because it uses a symmetric key, meaning the same key is used for both encryption and decryption. This key must be kept secret and only known by authorized parties. This simplicity makes Fernet easy to use while maintaining strong security.



