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
    if not notes:
        return 1

    last_note = notes[-1]
    return last_note["id"] + 1
