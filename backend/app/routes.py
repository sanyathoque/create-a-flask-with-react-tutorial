"""
This file contains the API routes.

React calls these routes with HTTP requests.
Flask responds with JSON.

Core pattern:

    Route receives the request.
    request.get_json() reads incoming JSON when needed.
    Python logic works with the data.
    jsonify() sends JSON back.
"""

from flask import Blueprint, jsonify, request

from .data import notes, get_next_note_id


# Blueprint groups related routes together.
# This blueprint is registered in app/__init__.py with url_prefix="/api".
# So every route in this file starts with /api in the browser.
api = Blueprint("api", __name__)


@api.get("/health")
def health_check():
    """
    Check if the backend server is running.

    Full URL:

        GET /api/health

    This route is useful because React, Postman, curl, or a browser can
    quickly confirm that Flask is alive.
    """

    # jsonify() converts the Python dictionary into a JSON response.
    # The 200 status code means "OK, the request worked".
    return jsonify(
        {
            "status": "ok",
            "message": "Flask API is running.",
        }
    ), 200


@api.get("/notes")
def get_notes():
    """
    Return all notes.

    Full URL:

        GET /api/notes

    React would use this route to display a list of notes.
    """

    # Return both the notes list and a count.
    # This gives the frontend the data plus useful metadata.
    return jsonify(
        {
            "notes": notes,
            "count": len(notes),
        }
    ), 200


@api.get("/notes/<int:note_id>")
def get_note(note_id):
    """
    Return one note by ID.

    Full URL example:

        GET /api/notes/1

    <int:note_id> means:

        Take the number from the URL and pass it into this function
        as the note_id argument.
    """

    # Search through the notes list one note at a time.
    for note in notes:
        # If the current note's ID matches the URL ID, return that note.
        if note["id"] == note_id:
            return jsonify(note), 200

    # If the loop finishes without finding a note, return 404.
    # 404 means "not found".
    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404


@api.post("/notes")
def create_note():
    """
    Create a new note.

    Full URL:

        POST /api/notes

    Expected JSON body:

        {
            "title": "My title",
            "body": "My note body"
        }

    This route reads JSON from the request, validates it, creates a new
    note dictionary, stores it in the notes list, and returns the new note.
    """

    # Read the JSON body sent by the client.
    # If React sends JSON, this becomes a Python dictionary.
    data = request.get_json()

    # If there is no JSON body, the client sent a bad request.
    # 400 means "bad request".
    if not data:
        return jsonify(
            {
                "error": "Request body must be JSON."
            }
        ), 400

    # Safely read the title and body fields.
    # .get("title") returns None if "title" is missing.
    # That is safer than data["title"], which would crash if missing.
    title = data.get("title")
    body = data.get("body")

    # A valid note needs both title and body.
    if not title or not body:
        return jsonify(
            {
                "error": "Both title and body are required."
            }
        ), 400

    # Build the new note dictionary.
    # get_next_note_id() creates the next ID from the current list.
    new_note = {
        "id": get_next_note_id(),
        "title": title,
        "body": body,
    }

    # Save the note in the fake in-memory database.
    notes.append(new_note)

    # Return the created note.
    # 201 means "created successfully".
    return jsonify(new_note), 201


@api.put("/notes/<int:note_id>")
def update_note(note_id):
    """
    Update an existing note.

    Full URL example:

        PUT /api/notes/1

    Expected JSON body can include title, body, or both:

        {
            "title": "Updated title"
        }

    This route finds the note by ID and updates only the fields sent
    by the client.
    """

    # Read JSON sent by the client.
    data = request.get_json()

    # Updating needs a JSON body.
    if not data:
        return jsonify(
            {
                "error": "Request body must be JSON."
            }
        ), 400

    # Find the note with the matching ID.
    for note in notes:
        if note["id"] == note_id:
            # data.get("title", note["title"]) means:
            #
            #   Use the new title if the client sent one.
            #   Otherwise keep the old title.
            note["title"] = data.get("title", note["title"])

            # Same idea for body:
            # use the new body if present, otherwise keep the old body.
            note["body"] = data.get("body", note["body"])

            # Return the updated note with 200 OK.
            return jsonify(note), 200

    # If no matching note was found, return 404.
    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404


@api.delete("/notes/<int:note_id>")
def delete_note(note_id):
    """
    Delete one note by ID.

    Full URL example:

        DELETE /api/notes/1

    This route searches for the note, removes it from the notes list,
    and returns a success message.
    """

    # Search for the note to delete.
    for note in notes:
        if note["id"] == note_id:
            # Remove the note from the fake database.
            notes.remove(note)

            # Return a confirmation message.
            return jsonify(
                {
                    "message": "Note deleted successfully."
                }
            ), 200

    # If the note ID does not exist, return 404.
    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404
