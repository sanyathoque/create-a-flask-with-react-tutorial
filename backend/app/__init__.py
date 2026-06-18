from flask import Flask
from flask_cors import CORS

from .routes import api


def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://localhost:3000",
                ]
            }
        },
    )

    app.register_blueprint(api, url_prefix="/api")

    return app
