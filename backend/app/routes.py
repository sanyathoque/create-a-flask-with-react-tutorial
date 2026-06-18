from flask import Blueprint, jsonify, request

from .data import notes, get_next_note_id


api = Blueprint("api", __name__)


@api.get("/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "message": "Flask API is running.",
        }
    ), 200


@api.get("/notes")
def get_notes():
    return jsonify(
        {
            "notes": notes,
            "count": len(notes),
        }
    ), 200


@api.get("/notes/<int:note_id>")
def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return jsonify(note), 200

    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404


@api.post("/notes")
def create_note():
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "Request body must be JSON."
            }
        ), 400

    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify(
            {
                "error": "Both title and body are required."
            }
        ), 400

    new_note = {
        "id": get_next_note_id(),
        "title": title,
        "body": body,
    }

    notes.append(new_note)

    return jsonify(new_note), 201


@api.put("/notes/<int:note_id>")
def update_note(note_id):
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "Request body must be JSON."
            }
        ), 400

    for note in notes:
        if note["id"] == note_id:
            note["title"] = data.get("title", note["title"])
            note["body"] = data.get("body", note["body"])

            return jsonify(note), 200

    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404


@api.delete("/notes/<int:note_id>")
def delete_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)

            return jsonify(
                {
                    "message": "Note deleted successfully."
                }
            ), 200

    return jsonify(
        {
            "error": "Note not found."
        }
    ), 404
