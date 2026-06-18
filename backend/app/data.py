"""
This file is the tiny fake data layer.

In a real app, this file would usually be replaced by a database.
For learning Flask routes, a Python list is easier to understand.

Important:

    The notes list is stored in memory.
    If the Flask server restarts, the notes reset.
"""

# This list pretends to be a database table.
# Each dictionary is one note.
# Dictionaries turn into JSON objects naturally when returned with jsonify().
notes = [
    {
        "id": 1,
        "title": "Learn Flask",
        "body": "Flask sends JSON to React.",
    },
    {
        "id": 2,
        "title": "Connect React",
        "body": "React calls Flask API endpoints.",
    },
]


def get_next_note_id():
    """
    Return the next ID for a new note.

    Example:

        If the last note has id 2,
        the next note should get id 3.

    This is simple learning logic, not production database logic.
    A real database would usually create IDs for you.
    """

    # If there are no notes, the first note should start at ID 1.
    if not notes:
        return 1

    # notes[-1] means "the last item in the notes list".
    last_note = notes[-1]

    # Take the last ID and add 1.
    return last_note["id"] + 1
