# Coding 2: Secure password storage

## Instructions
For this assessment, you have to write a small website that allows used to create an account and then
to connect to their account. Passwords of the users must be stored securely in the database, that is, in
hashed form.

Pay attention to the following elements:
* The design and content of the website served is not important.
* Use the suitable hash/encryption cryptographic tool to store the passwords.

Prepare yourself for the following manipulations/questions:
* Explain the role of hashing/encrypting passwords in a database regarding the CIA triad.
* Why is is so important to not store passwords in clear in a database?
* For such a system, is it necessary to have an HTTPS server?
* Think about the residual risks of hashing/encrypting all the passwords in the database.

## Install and run

1. Generate a virtual environment within the app folder and install the required packages:
```
$ python -m venv venv
$ venv\Scripts\activate
$ (venv) pip install -r requirements.txt
```
2. Generate the certificates for the TLS protocol, e.g., for Windows 10 with MINGW64 terminal:
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
3. When running the flask application, use a secure port (ex: 443) to catch the encrypted traffic with Wireshark:
```python
app.run(debug=True, ssl_context=context, port="443")
```
4. The first time you'll execute the script 'server.py' a database 'database.db' will be created (the corresponding code lines should be commented next time). You can download 'DB Browser Sqlite' to navigate its content.

5. Launch the script 'server.py' (This is a development server. Do not use it in production deployment) and follow the link https://127.0.0.1:443/.
