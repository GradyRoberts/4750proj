"""
Entry point for the app.
"""

from nfl_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
