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

## Notes

1. Generate virtual environment and install required packages:
```
$ python3 -m venv venv
$ pip install -r requirements.txt --no-index --find-links file:///tmp/packages
```

