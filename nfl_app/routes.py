"""
Includes all of the routes for the app.
"""

from flask import current_app as app
from flask import render_template, request, redirect, url_for, session


from nfl_app.passwords import hash_pwd, check_pwd
from nfl_app.users import add_new_user, remove_user, user_exists, fetch_user, fetch_all_users, is_admin


@app.route("/")
def index():
    fname = ""
    authenticated = False
    isAdmin = False
    if "authenticated" in session:
        if session["authenticated"]:
            if "email" in session:
                authenticated = True
                email = session["email"]
                fname = fetch_user(email)[0]
            isAdmin = is_admin(email)
            session["isAdmin"] = isAdmin
        print("permissions: ", authenticated, isAdmin)
    return render_template("index.html", authenticated=authenticated, fname=fname, isAdmin=isAdmin)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if user_exists(email):
            if check_pwd(email, password):
                session["authenticated"] = True
                if "email" not in session:
                    session["email"] = email
                if "isAdmin" not in session:
                    session["isAdmin"] = is_admin(email)
                print("user is admin: ", session["isAdmin"])
                return redirect(url_for("index"))
        else:
            print("user did not exist", email)
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



@app.route("/admin/removeuser", methods=["GET", "POST"])
def admin_remove_user():
    authenticated = False
    if request.method == "POST":
        if "authenticated" in session:
            if session["authenticated"]:
                authenticated = True
                user_email = request.form.get("email")
                remove_user(user_email)
                print("success")
        return redirect(url_for("index"))
    else:
        if "authenticated" in session and session["authenticated"]:
            authenticated = True
    return render_template("admin/removeuser.html", authenticated=authenticated)

@app.route("/admin/editplay", methods=["GET", "POST"])
def admin_remove_user():
    fields = {
        "new_game_id": "",
        "old_game_id": "",
        "new_desc": "",
        "new_play_type": "",
        "new_posteam": "",
        "new_posteam_type": "",
        "new_yards_gained": "",
        "new_side_of_field": "",
        "new_yrdln": "",
        "new_qtr": "",
        "new_time": "",
        "new_wp": "",
        "new_down": "",
        "new_ydstogo": ""
    }
    authenticated = False
    if request.method == "POST":
        if "authenticated" in session:
            if session["authenticated"]:
                authenticated = True
                for key in fields:
                    fields[key] = request.form.get(key)
                
                remove_user(user_email)
                print("success")
        return redirect(url_for("index"))
    else:
        if "authenticated" in session and session["authenticated"]:
            authenticated = True
    return render_template("admin/removeuser.html", authenticated=authenticated)