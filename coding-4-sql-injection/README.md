# Coding 4: SQL injection

## Instructions

For this assessment, you have to write a small command line application that allows the user to query
the content of a database. The input of the user should be inserted inside an SQL request and it should
be able to attack the database through an SQL injection. Also show how to protect your application
against SQL injection attacks.

Pay attention to the following elements:
* The design and content of the application is not important.
* An example of SQL injection could be that the user is able to filter returned data or is able to remove data in a table.

Prepare yourself for the following manipulations/questions:
* Show the malicious input that the user has to use and print the resulting SQL query that will be executed.
* How can your protect against SQL injection and why it works?
* What are the specific functions from the programming language/library you choose that are used to prevent SQL injection?
*    What is the drawback of writing more robust code regarding SQL injection?


## Install and run

1. Generate a virtual environment within the app folder and install the required packages:
```
$ python -m venv venv
$ venv\Scripts\activate
$ (venv) pip install -r requirements.txt
```
2. Launch the script 'server.py' (This is a development server. Do not use it in production deployment) and follow the link https://127.0.0.1:5000/



--------------------

## Exemples

In the following example, the input of the user is **not filtered** for ESCAPE CHARACTERS. Thus the user can inject some "code" that will modify the SQL statement.

```SQL
sql = "SELECT * FROM users WHERE name='{}' AND password='{}';".format(user, pwd)
```

In this case the user could put somehting like **b' OR '1=1** as the password and it would always match.

--------------------

http://127.0.0.1:5000/users?role=user' OR '1'='1

Permet d'obtenir la liste de tous les utilisateurs, même ceux qui sont de status 'admin' alors qu'en backend, le code est supposé bloquer l'affichage des administrateurs:
```python
def list_users():
    role = request.args.get('role', '')

    if role == 'admin':
        return "Can't list admins!"

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT username, role FROM users WHERE role = '{}'".format(role))
        data = cur.fetchall()
        return str(data)
```

from https://rushter.com/blog/detecting-sql-injections-in-python/


Une manière simple de corriger 'à la main' le problème ici est de  **d'abord de vérifier la valeur** passée au paramètre 'role' (qui ne peut prendre que quelques valeurs prédéfinies) avant d'exécuter la requête SQL. Cela peut se faire au moyen d'une expression régulière, de listes,... par exemple:

```python
def list_users():
    role = request.args.get('role', '')
    list_roles = ('moderator', 'user')

    if role == 'admin':
        return "Can't list admins!"
    elif role in list_roles:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username, role FROM users WHERE role = '{}'".format(role))
            data = cur.fetchall()
            return str(data)
    else:
        return "Wrong parameter"
```


Autrement, il est également possible d'uiliser une requête avec des paramètres liés (*parametrized query* / *bind-parameters*)
```python
cur.execute("SELECT username, role FROM users WHERE role = ? ", (role,))
```

Finalement, il existe également des méthodes propres au langages utilisé qui permettent de controler automatiquement les injections de contenu:

