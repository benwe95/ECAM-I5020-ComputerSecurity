from flask import Flask, render_template, request, jsonify
import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        user=request.form['username']
    return 'Hello {}!'.format(user)

if __name__ == "__main__":
    # The certificate and key must be generated
    # For Windows with MINGW64 terminal: 
    # openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    context = ('cert.pem', 'key.pem')
    app.run(debug=True, ssl_context=context, port="443") # HTTPs