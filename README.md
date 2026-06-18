# Flask Backend for a React App

A friendly, memorable Flask tutorial for people who already know React.

**Goal:** Build a Flask API that React can call.

No React code here. Only Flask.

---

## Mental Model

Think of your full-stack app like this:

```text
React = the screen
Flask = the waiter
Database / data = the kitchen
```

React asks for data.

Flask receives the request, talks to the data layer, and sends JSON back.

The rule to memorize:

```text
Route receives.
Request reads.
Logic works.
JSON responds.
```

---

## Project Structure

```text
flask-react-api/
|
├── backend/
|   ├── app/
|   |   ├── __init__.py
|   |   ├── routes.py
|   |   └── data.py
|   |
|   ├── run.py
|   ├── requirements.txt
|   └── .env
|
└── frontend/
    └── your-react-app-here
```

We are only writing the `backend/` code.

---

## 1. Create the Backend Folder

```bash
mkdir flask-react-api
cd flask-react-api

mkdir backend
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows
.venv\Scripts\activate
```

Install Flask tools:

```bash
pip install Flask flask-cors python-dotenv
```

Save your dependencies:

```bash
pip freeze > requirements.txt
```

Your `requirements.txt` will look something like this:

```text
Flask
flask-cors
python-dotenv
```

---

## 2. Create `run.py`

File:

```text
backend/run.py
```

Code:

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

### Explanation

```python
from app import create_app
```

This imports the app factory function from the `app` package.

A factory is just a function that builds your Flask app.

```python
app = create_app()
```

This creates the actual Flask application.

```python
if __name__ == "__main__":
    app.run(debug=True)
```

This means:

```text
Only run the server directly when this file is executed.
```

`debug=True` is useful while learning because Flask restarts automatically when you change code and shows helpful errors.

Do not use `debug=True` in production.

---

## 3. Create the Flask App Factory

Create this file:

```text
backend/app/__init__.py
```

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

### Explanation

```python
from flask import Flask
```

This imports Flask itself.

`Flask` is the object that represents your backend application.

```python
from flask_cors import CORS
```

This imports CORS support.

CORS matters because your React app and Flask app usually run on different ports.

Example:

```text
React: http://localhost:5173
Flask: http://localhost:5000
```

The browser treats those as different origins.

So Flask must explicitly allow React to talk to it.

```python
from .routes import api
```

This imports our API routes from `routes.py`.

The dot means:

```text
Import from the current package.
```

```python
def create_app():
```

This function creates and configures the Flask app.

This pattern is called the application factory pattern.

It keeps your project cleaner than putting everything in one giant file.

```python
app = Flask(__name__)
```

This creates the Flask app.

`__name__` helps Flask know where your app lives.

```python
CORS(...)
```

This allows React to call your Flask API.

```python
resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:3000",
        ]
    }
}
```

This says:

```text
Only allow CORS for routes that start with /api/.
```

And only allow calls from these React development origins:

```text
http://localhost:5173
http://localhost:3000
```

`5173` is common for Vite.

`3000` is common for Create React App or other dev setups.

```python
app.register_blueprint(api, url_prefix="/api")
```

This connects the routes from `routes.py` to the app.

Every route inside the blueprint will start with:

```text
/api
```

So if the route is:

```text
/notes
```

The full URL becomes:

```text
/api/notes
```

```python
return app
```

This gives the finished Flask app back to `run.py`.

---

## 4. Create a Tiny Data Layer

Create this file:

```text
backend/app/data.py
```

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

### Explanation

This file pretends to be a database.

For now, we are storing notes in a Python list.

```python
notes = [...]
```

Each note is a dictionary.

A dictionary turns into JSON very naturally.

```python
def get_next_note_id():
```

This function gives every new note a unique ID.

```python
if not notes:
    return 1
```

If the list is empty, the first note should have ID `1`.

```python
last_note = notes[-1]
return last_note["id"] + 1
```

This looks at the last note and adds `1` to its ID.

This is not real database logic, but it is perfect for learning Flask API structure.

---

## 5. Create the API Routes

Create this file:

```text
backend/app/routes.py
```

Code:

```python
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
```

---

## 6. Understanding `routes.py`

### Importing Flask Tools

```python
from flask import Blueprint, jsonify, request
```

You are importing three important tools.

### `Blueprint`

A `Blueprint` lets you group routes together.

Instead of putting every route directly on the app, you put them inside a smaller route group.

Memorize it like this:

```text
Flask app = whole building
Blueprint = one room inside the building
```

### `jsonify`

`jsonify` turns Python dictionaries and lists into JSON responses.

React likes JSON.

So most Flask + React APIs return JSON.

### `request`

`request` lets Flask read incoming data.

For example, when React sends a POST request with JSON, Flask reads it using:

```python
request.get_json()
```

---

## Creating the Blueprint

```python
api = Blueprint("api", __name__)
```

This creates a route group named `api`.

Later, in `__init__.py`, we attach this blueprint to the main app:

```python
app.register_blueprint(api, url_prefix="/api")
```

So this route:

```python
@api.get("/notes")
```

Becomes this full URL:

```text
/api/notes
```

---

## 7. The Health Check Route

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

This route is for checking if the backend is alive.

Visit:

```text
http://localhost:5000/api/health
```

You should see:

```json
{
  "status": "ok",
  "message": "Flask API is running."
}
```

The `200` means success.

---

## 8. Get All Notes

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

This route returns every note.

React would call:

```text
GET /api/notes
```

The response looks like:

```json
{
  "notes": [
    {
      "id": 1,
      "title": "Learn Flask",
      "body": "Flask sends JSON to React."
    }
  ],
  "count": 1
}
```

Important pattern:

```text
Function gets data.
jsonify sends data.
Status code explains result.
```

---

## 9. Get One Note

```python
@api.get("/notes/<int:note_id>")
def get_note(note_id):
```

This route has a URL parameter.

Example:

```text
/api/notes/1
```

Flask takes the `1` from the URL and passes it into the function as `note_id`.

```python
<int:note_id>
```

This means:

```text
Only match this route if note_id is an integer.
```

Then we search for the note:

```python
for note in notes:
    if note["id"] == note_id:
        return jsonify(note), 200
```

If found, return it.

If not found:

```python
return jsonify(
    {
        "error": "Note not found."
    }
), 404
```

`404` means:

```text
The thing you asked for does not exist.
```

---

## 10. Create a Note

```python
@api.post("/notes")
def create_note():
```

This route creates a new note.

React would call:

```text
POST /api/notes
```

With JSON like:

```json
{
  "title": "New note",
  "body": "This came from React."
}
```

Flask reads the JSON:

```python
data = request.get_json()
```

Then we validate it:

```python
if not data:
    return jsonify(
        {
            "error": "Request body must be JSON."
        }
    ), 400
```

`400` means:

```text
The client sent a bad request.
```

Then we pull out the fields:

```python
title = data.get("title")
body = data.get("body")
```

`.get()` is safer than direct access.

This:

```python
data.get("title")
```

will return `None` if `title` does not exist.

This:

```python
data["title"]
```

would crash if `title` does not exist.

Then we validate again:

```python
if not title or not body:
```

Both fields are required.

Then we create the note:

```python
new_note = {
    "id": get_next_note_id(),
    "title": title,
    "body": body,
}
```

Then store it:

```python
notes.append(new_note)
```

Then respond:

```python
return jsonify(new_note), 201
```

`201` means:

```text
Created successfully.
```

---

## 11. Update a Note

```python
@api.put("/notes/<int:note_id>")
def update_note(note_id):
```

This route updates an existing note.

React would call:

```text
PUT /api/notes/1
```

With JSON like:

```json
{
  "title": "Updated title"
}
```

The code:

```python
note["title"] = data.get("title", note["title"])
note["body"] = data.get("body", note["body"])
```

This means:

```text
Use the new value if React sent one. Otherwise, keep the old value.
```

Example:

```python
data.get("title", note["title"])
```

If `title` exists in the request, use it.

If not, keep the current title.

This makes partial updates easier.

---

## 12. Delete a Note

```python
@api.delete("/notes/<int:note_id>")
def delete_note(note_id):
```

This route deletes a note.

React would call:

```text
DELETE /api/notes/1
```

We search for the note:

```python
for note in notes:
    if note["id"] == note_id:
```

Then remove it:

```python
notes.remove(note)
```

Then return a success message:

```python
return jsonify(
    {
        "message": "Note deleted successfully."
    }
), 200
```

---

## 13. Run the Flask Server

From inside the `backend/` folder:

```bash
python run.py
```

You should see something like:

```text
Running on http://127.0.0.1:5000
```

Test this in your browser:

```text
http://localhost:5000/api/health
```

---

## 14. API Endpoint Summary

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Check if Flask is running |
| GET | `/api/notes` | Get all notes |
| GET | `/api/notes/<id>` | Get one note |
| POST | `/api/notes` | Create a note |
| PUT | `/api/notes/<id>` | Update a note |
| DELETE | `/api/notes/<id>` | Delete a note |

---

## 15. How React Connects Conceptually

No React code, just the contract.

Your React app should call Flask at:

```text
http://localhost:5000/api/...
```

Examples:

```text
GET    http://localhost:5000/api/notes
POST   http://localhost:5000/api/notes
PUT    http://localhost:5000/api/notes/1
DELETE http://localhost:5000/api/notes/1
```

The request body for creating a note should be JSON:

```json
{
  "title": "My title",
  "body": "My note body"
}
```

The request body for updating a note can be JSON:

```json
{
  "title": "Updated title",
  "body": "Updated body"
}
```

Your React app should send:

```text
Content-Type: application/json
```

Flask receives that JSON with:

```python
request.get_json()
```

Flask sends JSON back with:

```python
jsonify(...)
```

That is the whole connection.

---

## 16. Common Mistakes

### Mistake 1: Forgetting CORS

If React says something like:

```text
blocked by CORS policy
```

Your Flask backend probably has not allowed your React origin.

Check this part:

```python
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
```

### Mistake 2: Forgetting `/api`

This route:

```python
@api.get("/notes")
```

is not:

```text
/notes
```

Because we registered the blueprint with:

```python
url_prefix="/api"
```

So the actual route is:

```text
/api/notes
```

### Mistake 3: Sending Non-JSON Data

This expects JSON:

```python
data = request.get_json()
```

So the client must send:

```text
Content-Type: application/json
```

And the body must be valid JSON.

### Mistake 4: Expecting Data to Save Forever

Right now, notes are stored in a Python list.

When the Flask server restarts, the notes reset.

That is normal.

To save data permanently, use a database later.

Good next options:

- SQLite
- PostgreSQL
- MongoDB

For learning Flask, the list is enough.

---

## 17. The Flask Pattern to Memorize

Almost every Flask API route follows this shape:

```python
@api.method("/some-route")
def function_name():
    data = request.get_json()

    # validate data

    # do the work

    return jsonify(result), status_code
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

## 18. Final Backend Code Recap

### `backend/run.py`

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

### `backend/app/__init__.py`

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

### `backend/app/data.py`

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

### `backend/app/routes.py`

```python
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
```

---

## 19. What You Should Remember

The most important Flask ideas for React developers are:

- Flask serves API routes.
- React calls those routes.
- Flask reads JSON with `request.get_json()`.
- Flask returns JSON with `jsonify()`.
- CORS allows React and Flask to talk during development.
- Blueprints keep routes organized.

The key Flask + React sentence:

```text
React owns the UI. Flask owns the API.
```
