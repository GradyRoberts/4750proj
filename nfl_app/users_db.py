"""
Functions that interface with the database related to users.
"""

from nfl_app.conndb import mysql


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
    cur.close()
    return rv != None


def retrieve_pwd_hash(email):
    if not user_exists(email):
        return None
    cur = mysql.connection.cursor()
    sql = """SELECT password_hash FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchone()
    cur.close()
    return rv[0]


def fetch_user(email):
    if not user_exists(email):
        return None
    cur = mysql.connection.cursor()
    sql = """SELECT * FROM Users WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchone()  # row as tuple (fname, lname, email, hashed_password)
    cur.close()
    return rv


def update_user(fname, lname, email, hashed_password):
    cur = mysql.connection.cursor()
    sql = """UPDATE Users SET first_name=%s, last_name=%s, email=%s, password_hash=%s WHERE email=%s"""
    cur.execute(sql, (fname, lname, email, hashed_password, email))
    mysql.connection.commit()
    cur.close()


def fetch_all_users():
    """
    for development purposes
    """
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    cur.close()
    return str(rv)


def save_play(email, game_id, play_id):
    cur = mysql.connection.cursor()
    sql = """INSERT INTO SavedPlays VALUES (%s, %s, %s)"""
    cur.execute(sql, (email, play_id, game_id))
    mysql.connection.commit()
    cur.close()


def unsave_play(email, game_id, play_id):
    cur = mysql.connection.cursor()
    sql = """DELETE FROM SavedPlays WHERE email=%s AND play_id=%s AND game_id=%s"""
    cur.execute(sql, (email, play_id, game_id))
    mysql.connection.commit()
    cur.close()


def fetch_saved_plays(email):
    cur = mysql.connection.cursor()
    sql = """SELECT game_id, play_id FROM SavedPlays WHERE email=%s"""
    cur.execute(sql, (email,))
    rv = cur.fetchall()
    cur.close()
    return rv
