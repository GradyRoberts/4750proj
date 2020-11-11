from flask import current_app as app
from flask import render_template, request, redirect, url_for, session


from nfl_app.passwords import hash_pwd, check_pwd
from nfl_app.users import add_new_user, remove_user, user_exists, fetch_all_users


@app.route("/")
def index():
    return fetch_all_users()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if user_exists(email):
            if check_pwd(email, password):
                if "authenticated" not in session:
                    session["authenticated"] = True
                return redirect(url_for("index"))
        return render_template("login.html", error="Login failed.")
    return render_template("login.html", error="")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_pwd(password)
        add_new_user(fname, lname, email, hashed_password)
        return redirect(url_for("index"))
    return render_template("register.html")
