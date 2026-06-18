# Memorize the Flask Backend

Use this file as your daily review.

Read it in this order:

```text
run.py
app/__init__.py
app/data.py
app/routes.py
```

The whole app is one sentence:

```text
run.py starts Flask.
__init__.py builds Flask.
data.py stores fake data.
routes.py handles API requests.
```

---

## 1. The Whole Backend in Your Head

```text
React asks.
Flask route receives.
request reads JSON.
Python logic works.
jsonify sends JSON back.
```

Memorize this:

```text
Route receives.
Request reads.
Validate early.
Logic works.
JSON responds.
```

---

## 2. `backend/run.py`

Code:

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

Meaning:

```text
Import the app builder.
Build the app.
Run the server.
```

Line by line:

```python
from app import create_app
```

Go into the `app` folder and import the function named `create_app`.

```python
app = create_app()
```

Call that function and store the finished Flask app in `app`.

```python
if __name__ == "__main__":
```

Only run the next line when we directly run this file with:

```bash
python run.py
```

```python
app.run(debug=True)
```

Start the Flask server in learning mode.

Memorize:

```text
run.py is the start button.
```

---

## 3. `backend/app/__init__.py`

Code:

```python
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
```

Meaning:

```text
Create Flask.
Allow React with CORS.
Attach API routes.
Return the app.
```

Line by line:

```python
from flask import Flask
```

Import Flask, the main backend app object.

```python
from flask_cors import CORS
```

Import the tool that lets React call Flask from another port.

```python
from .routes import api
```

Import the route group from `routes.py`.

The dot means:

```text
Look inside this same app package.
```

```python
def create_app():
```

Define the function that builds the Flask app.

This is called the app factory pattern.

```python
app = Flask(__name__)
```

Create the Flask app.

```python
CORS(app, ...)
```

Allow browser requests from React development servers.

```python
r"/api/*"
```

Only apply CORS to API routes.

```python
"http://localhost:5173"
```

Vite React dev server.

```python
"http://localhost:3000"
```

Common React dev server.

```python
app.register_blueprint(api, url_prefix="/api")
```

Attach all routes from `routes.py`.

Every route now starts with `/api`.

So:

```text
/notes
```

becomes:

```text
/api/notes
```

```python
return app
```

Give the completed Flask app back to `run.py`.

Memorize:

```text
__init__.py builds and connects the app.
```

---

## 4. `backend/app/data.py`

Code:

```python
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
```

Meaning:

```text
Store fake notes.
Give new notes an ID.
```

Line by line:

```python
notes = [...]
```

This is our fake database.

Each note is a Python dictionary.

Python dictionary:

```python
{"id": 1, "title": "Learn Flask"}
```

JSON object:

```json
{"id": 1, "title": "Learn Flask"}
```

They look almost the same, which is why Flask APIs often return dictionaries as JSON.

```python
def get_next_note_id():
```

This function creates the next ID.

```python
if not notes:
    return 1
```

If the list is empty, start at ID `1`.

```python
last_note = notes[-1]
```

Get the last note in the list.

```python
return last_note["id"] + 1
```

Take the last ID and add `1`.

Memorize:

```text
data.py is the fake database.
```

---

## 5. `backend/app/routes.py`

This is the main file to memorize.

It has the API routes React will call.

Top of the file:

```python
from flask import Blueprint, jsonify, request

from .data import notes, get_next_note_id


api = Blueprint("api", __name__)
```

Meaning:

```text
Blueprint groups routes.
jsonify sends JSON.
request reads incoming data.
notes is the fake database.
```

### `Blueprint`

```python
api = Blueprint("api", __name__)
```

This creates a route group.

Memorize:

```text
Blueprint = a folder of routes.
```

### `jsonify`

```python
return jsonify(data), 200
```

This sends JSON back to React.

Memorize:

```text
jsonify = Python to JSON response.
```

### `request`

```python
data = request.get_json()
```

This reads JSON sent by React.

Memorize:

```text
request = what React sent.
```

---

## 6. Route: Health Check

```python
@api.get("/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "message": "Flask API is running.",
        }
    ), 200
```

URL:

```text
GET /api/health
```

Purpose:

```text
Check if Flask is alive.
```

Memorize:

```text
Health route says: server is running.
```

---

## 7. Route: Get All Notes

```python
@api.get("/notes")
def get_notes():
    return jsonify(
        {
            "notes": notes,
            "count": len(notes),
        }
    ), 200
```

URL:

```text
GET /api/notes
```

Purpose:

```text
Return all notes.
```

What it sends:

```python
{
    "notes": notes,
    "count": len(notes),
}
```

Memorize:

```text
GET all = return list and count.
```

---

## 8. Route: Get One Note

```python
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
```

URL:

```text
GET /api/notes/1
```

Purpose:

```text
Return one note by ID.
```

Important part:

```python
<int:note_id>
```

This takes the number from the URL and gives it to the function.

Example:

```text
/api/notes/5
```

becomes:

```python
note_id = 5
```

Memorize:

```text
URL number becomes function argument.
```

Status code:

```text
200 = found it
404 = could not find it
```

---

## 9. Route: Create a Note

```python
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
```

URL:

```text
POST /api/notes
```

Purpose:

```text
Create a new note.
```

Daily memory shape:

```text
Read JSON.
Validate JSON.
Get title and body.
Validate title and body.
Build new note.
Append to notes.
Return new note with 201.
```

Important line:

```python
data = request.get_json()
```

This reads the JSON body.

Important line:

```python
title = data.get("title")
body = data.get("body")
```

This safely reads fields.

`.get()` is safer than `data["title"]` because missing fields do not crash immediately.

Important line:

```python
notes.append(new_note)
```

This saves the note in the fake database.

Status code:

```text
201 = created
400 = bad request
```

Memorize:

```text
POST creates.
201 means created.
```

---

## 10. Route: Update a Note

```python
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
```

URL:

```text
PUT /api/notes/1
```

Purpose:

```text
Update an existing note.
```

Most important line:

```python
note["title"] = data.get("title", note["title"])
```

Meaning:

```text
Use the new title if it exists.
Otherwise keep the old title.
```

Same pattern:

```python
note["body"] = data.get("body", note["body"])
```

Memorize:

```text
PUT updates.
data.get(new, old) keeps old value if missing.
```

Status code:

```text
200 = updated
400 = bad request
404 = note missing
```

---

## 11. Route: Delete a Note

```python
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
```

URL:

```text
DELETE /api/notes/1
```

Purpose:

```text
Delete one note by ID.
```

Important line:

```python
notes.remove(note)
```

This removes the note from the fake database.

Memorize:

```text
DELETE removes.
404 means nothing to remove.
```

---

## 12. CRUD Memory Table

| Action | Method | Route | Flask Job |
| --- | --- | --- | --- |
| Check server | `GET` | `/api/health` | Return status |
| Read all | `GET` | `/api/notes` | Return list |
| Read one | `GET` | `/api/notes/1` | Find by ID |
| Create | `POST` | `/api/notes` | Read JSON and append |
| Update | `PUT` | `/api/notes/1` | Find by ID and change |
| Delete | `DELETE` | `/api/notes/1` | Find by ID and remove |

Memorize:

```text
GET reads.
POST creates.
PUT updates.
DELETE removes.
```

---

## 13. Status Code Memory Table

| Code | Meaning | Use |
| --- | --- | --- |
| `200` | OK | Request worked |
| `201` | Created | New note created |
| `400` | Bad Request | Client sent bad or missing JSON |
| `404` | Not Found | Note ID does not exist |

Memorize:

```text
200 worked.
201 created.
400 bad input.
404 missing thing.
```

---

## 14. Daily 2-Minute Review

Say this out loud:

```text
run.py starts the app.
__init__.py creates the app, enables CORS, and registers routes.
data.py stores the fake notes list.
routes.py defines what happens when React calls the API.
```

Then say this:

```text
GET reads data.
POST creates data.
PUT updates data.
DELETE removes data.
```

Then say this:

```text
request.get_json() reads JSON from React.
jsonify() sends JSON back to React.
Blueprint groups routes.
CORS lets React and Flask talk.
```

Final sentence:

```text
React owns the UI. Flask owns the API.
```
