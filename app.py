import os

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv

from passwords import hash_pwd, check_pwd


app = Flask(__name__)

load_dotenv("settings.env")

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    cur.close()
    return str(rv)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hash_pwd(password)

        cur = mysql.connection.cursor()
        sql = """INSERT INTO Users VALUES (%s,%s,%s,%s)"""
        cur.execute(sql, (fname, lname, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
