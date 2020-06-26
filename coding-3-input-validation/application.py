import click
import os
import sqlite3
import re
from datetime import datetime

#This list corresponds to the number of days in each month 
#January, February, Mars, April, May, June, July, August, September, October, November, December
MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DATABASE = 'database.db'

def db_create():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("""CREATE TABLE users (id integer primary key autoincrement,
                                       name TEXt,
                                       pseudo TEXT,
                                       birthday DATE,
                                       phone TEXT)
                                       
                """)

    #cur.execute("INSERT INTO users (name, pseudo, birthday, phone) VALUES (?, ?, ?, ?)", (ben, boubouule, , ))
    #cur.execute("INSERT INTO users (name, pseudo, birthday, phone) VALUES (?, ?, ?, ?)", (, , , ))
    #cur.execute("INSERT INTO users (name, pseudo, birthday, phone) VALUES (?, ?, ?, ?)", (, , , ))
    con.commit()

@click.command()
@click.option('--count', default=1, help='Number of greetings')
@click.option('--name', prompt='Your name', help='The person to greet')
def hello(count, name):
    for x in range (count):
        click.echo('Hello %s' % name)

@click.command()
@click.option('--name', prompt='Your name', help='The person to greet')
@click.option('--pseudo', prompt='Your pseudo', help='Any alpha-nuremical sequence of caracter (no special caract [(\'\"!?]_-)] ')
@click.option('--birthday', prompt='Your birthday (dd/MM/YY)', help='The date of your birthday: format should be dd/mm/YYYY')
@click.option('--phone', prompt='Your phone number', help='Format should be xxxxxxxxx - x between 0 and 9')
def registration(name, pseudo, birthday, phone):
    count_tries = 0
    is_valid = True

    is_valid = check_name(name)

    if is_valid:
        is_valid = check_pseudo(pseudo)
    else:
        registration()

    if is_valid:
        is_valid = check_birthday_regex(birthday)
    else:
        registration()
    
    if is_valid:
        is_valid = check_phone(phone)
    else:
        registration()


    if is_valid:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(name, birthday, phone) VALUES (?, ?, ?)", (name, birthday, phone))
            con.commit()
            click.echo('You have been register as: %s' %name)
    else:
        registration()

def check_pseudo(pseudo):
    print(pseudo)
    is_valid = False
    try:
        if (re.match('\w', pseudo)):
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE pseudo = ?", (pseudo))
                data = cur.fetchall()
            if data:
                click.echo("Pseudo already exists!")
            else:
                click.echo("Pseudo is valid")
                is_valid = True
    except Exception as e:
        click.echo(repr(e))
    return is_valid

def check_name(name):
    # Match tous les noms et noms composés (avec ou sans tiret, max 2)
    pattern = "^[a-zA-Z]+[ -]?[a-zA-Z]*$"
    if (re.match(pattern, name)):
        click.echo("'%s' is a valid name" %name)
        return True
    click.echo('Wrong name')
    return False

#-------------------------------------------
#------------- DATE ------------------------
#-------------------------------------------

"""Vérficication de la date en utilisant une expression régulière """
def check_birthday_regex(birthday):
    pattern = "^\d{2}\/\d{2}\/\d{4}$"
    if re.match(pattern, birthday):
        numbers = birthday.split('/')
        if int(numbers[1]) not in range(1, 13):
            click.echo('The month should be an integer between 01 and 12')
            return False
        elif int(numbers[0]) not in range(1, MONTHS[int(numbers[1])-1]+1):
            click.echo("The day should be an integer between 1 and {}".format(MONTHS[int(numbers[1])-1]))
            return False
        elif int(numbers[2]) not in range(0, 2020):
            click.eco("The year is wrong")
            return False
        else:
            click.echo("%s is a valid date." %birthday)
            return True
    else:   
        click.echo("Error - The format of the date should be dd/mm/YYYY")
        return False

""" Vérification de la date en utilisant l'objet datetime """
def check_birthday_object(birthday):
    date_splited = datetime.strptime(birthday, "%d/%m/%Y")
    return (birthday, date_splited)

def check_phone(phone):
    pattern = "0\d{9}"
    is_valid = False
    return (is_valid, 'Wrong Phone number. Format should be 0XXXXXXXX [0-9]')

if __name__ == '__main__':
    
    #db_create()
    registration()

    #dates = ["01/01/1995", "1/01/1995", "01/1/1995", "01/01/1", "01/01/12", "abcd", "01/qv/1995", "b/01/1995",
    #         "01/01/abcd", "01/01/2021", "02/13/1993", "00/12/1992", "12/00/1993", "32/12/2004", "12/02/2021"]
    #for date in dates:
    #    #res = check_birthday(date)
    #    try:
    #        res = check_birthday_object(date)
    #        print("{}\n\t{}".format(date, res[1]))
    #    except ValueError as error:
    #        print(error) 
        