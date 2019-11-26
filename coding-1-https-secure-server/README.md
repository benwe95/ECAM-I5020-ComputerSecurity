# Coding 1: HTTPS secure server

## Instructions

For this assessment, you have to write a small web server that distributes one page with a form that
can be filled by the user and whose data are sent back to the server. This server must be first served
over HTTP and then modified to be served over HTTPS.
Pay attention to the following elements:

* The design and content of the website served is not important.
* Use a password input field in the form.

Prepare yourself for the following manipulations/questions:
* Show how data filled in the form can be eavesdropped with the HTTP server and are hidden
with the HTTPS server, using the Wireshark tool.
* Explain the role of an HTTPS server regarding the CIA triad.
* Think about the residual risks of putting an HTTPS server in place, instead of a simpler HTTP
server.

## Install and run

1. Generate a virtual environment within the app folder and install the required packages:
```
$ python -m venv venv
$ venv\Scripts\activate
$ (venv) pip install -r requirements.txt
```
2. Generate the cerficates for the TLS protocole. Ex for Windows 10 with MINGW64 terminal:
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
3. Use a secure port (ex: 443) to catch the encrypted traffic with Wireshark.

4. Launch the script 'server.py' (this is a development server. Do not use it in production deployment) and follow the [link https://127.0.0.1:443/] (https://127.0.0.1:443/).

5. Launch Wireshark and filter the traffic by searching 'tcp.port==443' or 'tls' in the options.

6. You can decrypt the traffic using the (Pre)-Master-Secret in Wireshark. Read the following tutorial about [Transport Layer Security (TLS)](https://wiki.wireshark.org/TLS?action=show&redirect=SSL) to configure it.