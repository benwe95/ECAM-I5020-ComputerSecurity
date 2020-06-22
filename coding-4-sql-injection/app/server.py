from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "data.db"

def db_create():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("""CREATE TABLE users (id integer primary key autoincrement, 
                                       username TEXT, 
                                       password TEXT,
                                       role TEXT)
                """)
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'pwdadmin', 'admin'))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('ben', 'pwdben', 'user'))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('bob', 'pwdbob', 'user'))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('markus', 'pwdmarkus', 'moderator'))

    con.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    print("Entered SIGNUP")
    if request.method == 'POST':
        try:
            username = request.form['username']
            pwd = request.form['password']
            role = "user"

            """
                Because the statement uses paramater binding : (username, password, role) VALUES (?, ?, ?)
                there can't be an injection here.
            """
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, pwd, role))
                con.commit()

        except e:
            print(e.message)
            con.rollback()

        finally:
            return 'Registration successful! Welcome {}!'.format(username)
    
    return 'Error no POST method found'


@app.route('/signin', methods=['POST'])
def signin_bad_sql():
    print('entered SIGNIN')
    access = False
    if request.method == 'POST':
        try:
            username = request.form['username']
            pwd= request.form['password']
            """
                SQL INJECTION is possible from here
            """
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                sql = "SELECT * FROM users WHERE username='{}' AND password='{}';".format(username, pwd)
                cur.execute(sql)
                print(sql)
                result = cur.fetchone()
                if result:
                    print(result)
                    access = True
                    username = result[0]
                else:
                    return "Incorrect username or password."
                
        except sqlite3.Error as error:
            print("Failed to read data from table", error)

        finally:
            return "Password corret! You are now connected as {}".format(username) if access else 'Wrong password!'

    return 'Error no POST method found'

def signin_good_sql():
    print('entered signin')
    access = False
    if request.method == 'POST':
        try:
            user = request.form['username']
            pwd_clear = request.form['password']
            pwd_hash_sha256 = hashlib.sha256(pwd_clear.encode())

            """
                SQL INJECTION is possible from here
            """
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                sql = "SELECT password FROM users_hash WHERE name={}".format(user)
                print("SQL: {}".format(sql))
                cur.execute('SELECT password FROM users_hash WHERE name=?', (user,))
                password = cur.fetchone()
                print("PWD from database: {}\nPWD from input: {}".format(password, pwd_hash_sha256.hexdigest()))
                if password[0]==pwd_hash_sha256.hexdigest(): 
                    access = True
                    print("PWD validated")

        except sqlite3.Error as error:
            print("Failed to read data from table", error)

        finally:
            return "Password corret! You are now connected as {}".format(user) if access else 'Wrong password!'


    return 'Error no POST method found'

@app.route("/user")
def about_user():
    user_id = request.args.get('id', '')
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.executescript("SELECT id, username, role FROM users WHERE id= {}".format(user_id))

@app.route("/users")
def list_users():
    role = request.args.get('role', '')

    if role == 'admin':
        return "Can't list admins!"
    
    """
    The statement is formatted as a string (no parameters binding) which is
    a vulnerability against SQLi.
    Here the 'role' variable is not escaped or preprocessed so we can inject 
    any SQL code in the query
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.executescript("SELECT id, username, role FROM users WHERE role = '{}'".format(role))
        data = cur.fetchall()
        return str(data)

@app.route("/users-corrected")
def list_users_corrected():
    role = request.args.get('role', '')
    list_roles = ('moderator', 'user')

    if role == 'admin':
        return "Can't list admins!"
    elif role in list_roles:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("SELECT id, username, role FROM users WHERE role = '{}'".format(role))
            data = cur.fetchall()
            return str(data)
    else:
        return "Wrong parameter"

@app.route("/users-corrected-2")
def list_users_corrected_2():
    role = request.args.get('role', '')

    if role == 'admin':
        return "Can't list admins!"

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT id, username, role FROM users WHERE role = ? ", (role,))
        data = cur.fetchall()
        return str(data)


if __name__ == "__main__":
    db_create()
    app.run(debug=True)
