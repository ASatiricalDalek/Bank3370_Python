import sqlite3
from flask import g

# Path is NOT relative
DATABASE = 'E:/Code/Python/Bank3370_Python/Bank3370.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def simpleQuery(table, row):
    cur = get_db().cursor()
    cur.execute("SELECT Id " + row + " FROM " + table)
    result = cur.fetchall()
    return result

