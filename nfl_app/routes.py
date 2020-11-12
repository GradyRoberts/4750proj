from flask import current_app as app
from flask import render_template, request, redirect, url_for, session


from nfl_app.passwords import hash_pwd, check_pwd
from nfl_app.users import add_new_user, remove_user, user_exists, fetch_user, fetch_all_users


@app.route("/")
def index():
    fname = ""
    authenticated = False
    if "authenticated" in session:
        if session["authenticated"]:
            if "email" in session:
                authenticated = True
                email = session["email"]
                fname = fetch_user(email)[0]
    return render_template("index.html", authenticated=authenticated, fname=fname)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if user_exists(email):
            if check_pwd(email, password):
                if "authenticated" not in session:
                    session["authenticated"] = True
                if "email" not in session:
                    session["email"] = email
                return redirect(url_for("index"))
        return render_template("login.html", error="Login failed.")
    return render_template("login.html", error="")


@app.route("/logout")
def logout():
    if "authenticated" in session:
        session["authenticated"] = False
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_pwd(password)
        add_new_user(fname, lname, email, hashed_password)
        return redirect(url_for("login"))
    return render_template("register.html")
