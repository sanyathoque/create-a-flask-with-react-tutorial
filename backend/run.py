"""
This file is the backend start button.

When you want to run the Flask API, you run:

    python run.py

This file does not define routes.
It only imports the Flask app builder, creates the app, and starts the server.
"""

from app import create_app

# create_app() lives in backend/app/__init__.py.
# It builds the Flask app, adds CORS, and connects the API routes.
app = create_app()

# __name__ is "__main__" only when this file is run directly.
# That means Flask starts only when you execute "python run.py".
# If another file imports this file, the server does not automatically start.
if __name__ == "__main__":
    # debug=True is for learning and development.
    # It reloads the server when code changes and shows helpful error pages.
    # Do not use debug=True in production.
    app.run(debug=True)
