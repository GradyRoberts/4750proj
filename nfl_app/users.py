from flask import current_app as app
from flask_mysqldb import MySQL


print(app.config['MYSQL_HOST'], app.config['MYSQL_PASSWORD'])

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
    return (rv != None)

def fetch_all_users():
    """
    for development purposes
    """
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    cur.close()
    return str(rv)