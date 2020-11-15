"""
Creates and configures the app context.
"""

import os


from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    with app.app_context():
        from . import routes

        return app
