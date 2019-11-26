from flask import Flask, render_template, request
import os
import hashlib
import sqlite3

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def db_connect(name):
    con = sqlite3.connect(name)
    print ("Opened database '{}' successfully".format(name))
    return con

def db_create(con, request):
    con.execute('CREATE TABLE {}'.format(request))
    print("Table created successfuly")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            user = request.form['username']
            pwd_clear = request.form['password']
            pwd_hash_sha256 = hashlib.sha256(pwd_clear.encode())

            print("user: {}:\npwd_clear: {}\npwd_md5: {}\npwd_sha: {}".format(
                user, pwd_clear, pwd_hash_md5.hexdigest(), pwd_hash_sha256.hexdigest()))
            

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users_clear (name, password) VALUES (?, ?)", (user, pwd_clear))
                cur.execute("INSERT INTO users_hash (name, password) VALUES (?, ?)", (user, pwd_hash_sha256.hexdigest()))
                con.commit()

        except:
            con.rollback()

        finally:
            con.close()
            return 'Registration successful! Welcome {}!'.format(user)
    
    return 'Error no POST method found'


@app.route('/signin', methods=['POST'])
def signin():
    print('entered signin')
    access = False
    if request.method == 'POST':
        try:
            user = request.form['username']
            pwd_clear = request.form['password']
            pwd_hash_sha256 = hashlib.sha256(pwd_clear.encode())

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('SELECT password FROM users_hash WHERE name=?', (user,))
                password = cur.fetchone()
                print("PWD from database: {}\nPWD from input: {}".format(password, pwd_hash_sha256.hexdigest()))
                if password[0]==pwd_hash_sha256.hexdigest(): 
                    access = True
                    print("PWD validated")

        except sqlite3.Error as error:
            print("Failed to read data from table", error)

        finally:
            con.close()
            return 'Hello {}! Your password is correct'.format(user) if access else 'Wrong password!'


    return 'Error no POST method found'

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')

    con = db_connect("database.db")
    db_create(con, "users_clear (name TEXT, password TXT)")
    db_create(con, "users_hash (name TEXT, password TXT)")

    app.run(debug=True, ssl_context=context, port="443")
