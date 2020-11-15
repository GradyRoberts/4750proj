"""
Includes all of the routes for the app.
"""
from io import StringIO
import csv


from flask import current_app as app
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    flash,
)


from nfl_app.passwords import hash_pwd, check_pwd
from nfl_app.users_db import (
    add_new_user,
    remove_user,
    user_exists,
    fetch_user,
    update_user,
    fetch_all_users,
    save_play,
    unsave_play,
    fetch_saved_plays,
    is_admin
)
from nfl_app.search_db import fetch_play
from nfl_app.search import perform_search

from nfl_app.plays_db import edit_play, add_play


@app.route("/")
def index():
    fname = ""
    username = ""
    email = ""
    authenticated = False
    isAdmin = False
    if request.cookies.get("authenticated")=="True":
        authenticated = True
        email = request.cookies.get("email")
        isAdmin = is_admin(email)
        fname = fetch_user(email)[0]
        username = email.split("@")[0]
    return render_template(
        "index.html",
        authenticated=authenticated,
        fname=fname,
        username=username,
        email=email,
        isAdmin=isAdmin
    )

# @app.route("/")
# def index():
#     fname = ""
#     username = ""
#     email = ""
#     authenticated = False
#     isAdmin = False
#     if "authenticated" in session:
#         if session["authenticated"]:
#             if "email" in session:
#                 authenticated = True
#                 email = session["email"]
#                 fname = fetch_user(email)[0]
#             isAdmin = is_admin(email)
#             session["isAdmin"] = isAdmin
#         print("permissions: ", authenticated, isAdmin)
#     return render_template("index.html", authenticated=authenticated, fname=fname, isAdmin=isAdmin)
#     if request.cookies.get("authenticated")=="True":
#         authenticated = True
#         email = request.cookies.get("email")
#         fname = fetch_user(email)[0]
#         username = email.split("@")[0]
#     return render_template(
#         "index.html",
#         authenticated=authenticated,
#         fname=fname,
#         username=username,
#         email=email,
#     )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if user_exists(email):
            if check_pwd(email, password):
                res = make_response(redirect(url_for("index")))
                res.set_cookie("authenticated", "True")
                res.set_cookie("email", email)
                res.set_cookie("isAdmin", str(is_admin(email)))
                return res
        return render_template("login.html", error="Login failed.")
    return render_template("login.html", error="")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#         if user_exists(email):
#             if check_pwd(email, password):
#                 session["authenticated"] = True
#                 if "email" not in session:
#                     session["email"] = email
#                 if "isAdmin" not in session:
#                     session["isAdmin"] = is_admin(email)
#                 print("user is admin: ", session["isAdmin"])
#                 return redirect(url_for("index"))
#         else:
#             print("user did not exist", email)
#         return render_template("login.html", error="Login failed.")
#     return render_template("login.html", error="")


@app.route("/logout")
def logout():
    res = make_response(redirect(url_for("index")))
    if "authenticated" in request.cookies:
        res.set_cookie("authenticated", "False")
    return res


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hash_pwd(password)
        try:
            add_new_user(fname, lname, email, hashed_password)
        except Exception as e:
            flash("UVA emails only!")
            return render_template("register.html", error="Invalid email.")
        return redirect(url_for("login"))
    return render_template("register.html", error="")


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.cookies.get("authenticated")=="False":
        return redirect(url_for("login"))
    email = request.args.get("email")
    if request.method == "POST":
        form_name = request.form.get("form_name")
        if form_name == "update_user":
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            password = request.form.get("password")
            hashed_password = hash_pwd(password)
            update_user(fname, lname, email, hashed_password)
        elif form_name == "delete_account":
            remove_user(email)
            return redirect(url_for("logout"))
    ids = fetch_saved_plays(email)
    rows = [fetch_play(game_id, play_id) for game_id, play_id in ids]
    return render_template("account.html", email=email, rows=rows)


@app.route("/save_play")
def save():
    if request.cookies.get("authenticated")=="False":
        return redirect(url_for("login"))
    email = request.args.get("email")
    game_id = request.args.get("game_id")
    play_id = request.args.get("play_id")
    save_play(email, game_id, play_id)
    return redirect(url_for("account", email=email))


@app.route("/unsave_play")
def unsave():
    if request.cookies.get("authenticated")=="False":
        return redirect(url_for("login"))
    email = request.args.get("email")
    game_id = request.args.get("game_id")
    play_id = request.args.get("play_id")
    unsave_play(email, game_id, play_id)
    return redirect(url_for("account", email=email))


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.cookies.get("authenticated")=="False":
        return redirect(url_for("login"))
    if request.method == "POST":
        rows, template = perform_search(request.form)
        if request.form.get("export"):
            si = StringIO()
            cw = csv.writer(si)
            cw.writerow(rows)
            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        email = request.cookies.get("email")
        return render_template(template, rows=rows, email=email)
    return render_template("search.html")



@app.route("/admin/removeuser", methods=["GET", "POST"])
def admin_remove_user():
    authenticated = False
    if request.cookies.get("authenticated")=="True":
        authenticated = True
    if request.method == "POST":
        if authenticated:
            user_email = request.form.get("email")
            remove_user(user_email)
        return redirect(url_for("index"))
    return render_template("admin/removeuser.html", authenticated=authenticated)

@app.route("/admin/editplay", methods=["GET", "POST"])
def admin_edit_play():
    fields = {
        "new_game_id": "",
        "new_play_id": "",
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
    if request.cookies.get("authenticated")=="True":
        authenticated = True
    if request.method == "POST":
        if authenticated:
            for key in fields:
                fields[key] = request.form.get(key)
            admin_edit_play(fields)
        return redirect(url_for("index"))
    return render_template("admin/editplay.html", authenticated=authenticated)
                

@app.route("/admin/addplay", methods=["GET", "POST"])
def admin_add_play():
    fields = {
        "game_id": "",
        "play_id": "",
        "desc": "",
        "play_type": "",
        "posteam": "",
        "posteam_type": "",
        "yards_gained": "",
        "side_of_field": "",
        "yrdln": "",
        "qtr": "",
        "time": "",
        "wp": "",
        "down": "",
        "ydstogo": ""
    }
    authenticated = False
    if request.cookies.get("authenticated")=="True":
        authenticated = True
    if request.method == "POST":
        if authenticated:
            for key in fields:
                fields[key] = request.form.get(key)
            admin_add_play(fields)
        return redirect(url_for("index"))
    return render_template("admin/addplay.html", authenticated=authenticated)


@app.route("/admin/deleteplay", methods=["GET", "POST"])
def admin_delete_play():
    authenticated = False
    if request.cookies.get("authenticated")=="True":
        authenticated = True
    if request.method == "POST":
        game_id = request.args.get("game_id")
        play_id = request.args.get("play_id")
        if authenticated:
            admin_delete_play(game_id, play_id)
        return redirect(url_for("index"))
    return render_template("admin/deleteplay.html", authenticated=authenticated)