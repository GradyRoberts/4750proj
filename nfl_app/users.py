"""
Functions that interface with the database related to users.
"""

from flask import current_app as app
from flask_mysqldb import MySQL


mysql = MySQL(app)


def add_new_user(fname, lname, email, hashed_password):
    cur = mysql.connection.cursor()
    sql = """INSERT INTO Users VALUES (%s,%s,%s,%s)"""
    cur.execute(sql, (fname, lname, email, hashed_password))
    mysql.connection.commit()
    cur.close()


def remove_user(email):
    cur = mysql.connection.cursor()
    sql = """DELETE FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    mysql.connection.commit()
    cur.close()


def user_exists(email):
    cur = mysql.connection.cursor()
    sql = """SELECT email FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchone()
    return rv != None


def retrieve_pwd_hash(email):
    if (not user_exists(email)):
        return None
    cur = mysql.connection.cursor()
    sql = """SELECT password_hash FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchone()
    return rv[0]


def fetch_user(email):
    if (not user_exists(email)):
        return None
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchone() # row as tuple (fname, lname, email, hashed_password)
    return rv 


def fetch_all_users():
    """
    for development purposes
    """
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    cur.close()
    return str(rv)
