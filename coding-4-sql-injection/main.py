#import click
import os
import sqlite3
import re
from datetime import datetime

def db_connect(name):
    con = sqlite3.connect(name)
    print ("Opened database '{}' successfully".format(name))
    return con

def db_create(con, request):
    con.execute('CREATE TABLE {}'.format(request))
    print("Table created successfuly")

def add_data(name, birthday, phone):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        con.execute("INSERT INTO users(name, birthday, phone) VALUES (?, ?, ?)", (name, birthday, phone))
        con.commit()

if __name__=='__main__':
    con = db_connect('database.db')
    #db_create(con, 'users (name TEXT, birthday DATE, phone TEXT)')



