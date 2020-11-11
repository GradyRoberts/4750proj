from flask import Flask, render_template, request, redirect, url_for, session


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    with app.app_context():
        from . import routes

        return app
