"""
This file builds the Flask application.

The important idea:

    run.py asks create_app() for a ready-to-use Flask app.

create_app() does three jobs:

    1. Create the Flask app.
    2. Allow React to call Flask with CORS.
    3. Register the API routes from routes.py.
"""

from flask import Flask
from flask_cors import CORS

from .routes import api


def create_app():
    """
    Build and return the Flask app.

    This is called the application factory pattern.
    "Factory" just means a function that creates something.

    Here, create_app() creates the Flask backend.
    """

    # Flask(__name__) creates the backend application object.
    # __name__ tells Flask where this app package lives.
    app = Flask(__name__)

    # CORS lets browser apps on other origins call this backend.
    #
    # React usually runs on one port:
    #   http://localhost:5173  for Vite
    #   http://localhost:3000  for many other React dev servers
    #
    # Flask usually runs on:
    #   http://localhost:5000
    #
    # Because the ports are different, the browser treats them as
    # different origins. CORS is the permission that says:
    #
    #   "These React origins are allowed to call my Flask API."
    CORS(
        app,
        resources={
            # Only routes that start with /api/ get this CORS rule.
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://localhost:3000",
                ]
            }
        },
    )

    # A blueprint is a group of routes.
    #
    # routes.py defines routes like:
    #   /health
    #   /notes
    #
    # url_prefix="/api" adds /api in front of every route.
    #
    # So /notes becomes:
    #   /api/notes
    app.register_blueprint(api, url_prefix="/api")

    # Give the finished Flask app back to run.py.
    return app
