# Flask Backend for a React App

A clear, memorable Flask tutorial for React developers.

You already know React, so this guide focuses only on the Flask side: routes, JSON, CORS, request data, errors, and a clean project shape.

## The Big Idea

React is the frontend.

Flask is the backend.

They talk through HTTP:

```text
React fetch()  --->  Flask route
React state    <---  Flask JSON response
```

Think of Flask as a small restaurant kitchen:

- A route is the menu item.
- A request is the customer order.
- A response is the finished plate.
- JSON is the shared language between React and Flask.

## Project Structure

Use this shape for a simple Flask API:

```text
backend/
  app.py
  requirements.txt
```

React can live somewhere else, usually:

```text
frontend/
  src/
  package.json
```

This tutorial only writes the Flask files.

## Install Flask

Inside your backend folder:

```bash
mkdir backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install flask flask-cors
pip freeze > requirements.txt
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Minimal Flask App

Create `backend/app.py`:

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.get("/")
def home():
    return jsonify({
        "message": "Flask API is running"
    })


if __name__ == "__main__":
    app.run(debug=True)
```

Run it:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

You should see JSON:

```json
{
  "message": "Flask API is running"
}
```

## Explain the Code

```python
from flask import Flask, jsonify
```

This imports the two Flask tools you use most at the beginning.

`Flask` creates the app.

`jsonify` turns Python dictionaries into proper JSON responses.

```python
from flask_cors import CORS
```

This imports CORS support.

React usually runs on a different port, like `http://localhost:3000` or `http://localhost:5173`.

Flask usually runs on `http://127.0.0.1:5000`.

Because those are different origins, the browser blocks requests unless Flask allows them. `CORS(app)` allows React to call your Flask API during development.

```python
app = Flask(__name__)
```

This creates your Flask application.

Memorize it as:

```text
app = my backend server
```

```python
CORS(app)
```

This tells Flask:

```text
Allow browser apps from other origins to call this API.
```

```python
@app.get("/")
def home():
```

This creates a GET route.

When the browser visits `/`, Flask runs the `home` function.

Memorize the pattern:

```python
@app.get("/some-url")
def some_function():
    return something
```

```python
return jsonify({
    "message": "Flask API is running"
})
```

This sends JSON back to React.

React receives this like any other API response.

```python
if __name__ == "__main__":
    app.run(debug=True)
```

This runs the Flask server when you execute:

```bash
python app.py
```

`debug=True` is helpful while learning because Flask reloads when you edit code and shows useful error messages.

Do not use `debug=True` in production.

## Add a Route That Returns Data

React often needs lists of data.

Add this to `app.py`:

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


posts = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Connect Flask to React", "done": False},
    {"id": 3, "title": "Build a full-stack app", "done": False},
]


@app.get("/")
def home():
    return jsonify({
        "message": "Flask API is running"
    })


@app.get("/api/posts")
def get_posts():
    return jsonify(posts)


if __name__ == "__main__":
    app.run(debug=True)
```

Visit:

```text
http://127.0.0.1:5000/api/posts
```

You should get:

```json
[
  {
    "id": 1,
    "title": "Learn Flask",
    "done": false
  },
  {
    "id": 2,
    "title": "Connect Flask to React",
    "done": false
  },
  {
    "id": 3,
    "title": "Build a full-stack app",
    "done": false
  }
]
```

## Explain the Data Route

```python
posts = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Connect Flask to React", "done": False},
    {"id": 3, "title": "Build a full-stack app", "done": False},
]
```

This is temporary in-memory data.

It acts like a tiny fake database while learning.

Important Python-to-JSON translation:

```text
Python False  ->  JSON false
Python True   ->  JSON true
Python None   ->  JSON null
```

```python
@app.get("/api/posts")
def get_posts():
    return jsonify(posts)
```

This says:

```text
When React asks GET /api/posts,
send back the posts list as JSON.
```

## Add a Route That Receives Data

To receive JSON from React, use `request`.

Update `app.py`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


posts = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Connect Flask to React", "done": False},
    {"id": 3, "title": "Build a full-stack app", "done": False},
]


@app.get("/")
def home():
    return jsonify({
        "message": "Flask API is running"
    })


@app.get("/api/posts")
def get_posts():
    return jsonify(posts)


@app.post("/api/posts")
def create_post():
    data = request.get_json()

    title = data.get("title")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "done": False
    }

    posts.append(new_post)

    return jsonify(new_post), 201


if __name__ == "__main__":
    app.run(debug=True)
```

## Explain the POST Route

```python
from flask import Flask, jsonify, request
```

`request` represents the incoming HTTP request.

Memorize it like this:

```text
request = what the client sent
```

```python
@app.post("/api/posts")
def create_post():
```

This creates a POST route.

Use POST when React is creating new data.

```python
data = request.get_json()
```

This reads the JSON body sent by React.

If React sends:

```json
{
  "title": "Practice Flask routes"
}
```

Then Flask sees:

```python
data = {
    "title": "Practice Flask routes"
}
```

```python
title = data.get("title")
```

This safely gets the `title` field.

Using `.get()` is friendlier than `data["title"]` because it does not crash if the key is missing.

```python
if not title:
    return jsonify({
        "error": "Title is required"
    }), 400
```

This validates the request.

If the title is missing, Flask returns:

- A JSON error message.
- HTTP status code `400`, meaning bad request.

Memorize:

```text
Bad client input -> 400
Created something -> 201
Everything okay -> 200
```

```python
new_post = {
    "id": len(posts) + 1,
    "title": title,
    "done": False
}
```

This creates a new Python dictionary.

Later, a real app would save this to a database.

For learning, appending to the list is enough.

```python
posts.append(new_post)
```

This stores the new post in memory.

Important: this data disappears when the Flask server restarts.

```python
return jsonify(new_post), 201
```

This sends the newly created post back to React.

The `201` status code means:

```text
Created successfully.
```

## Test the POST Route Without React

You can test the backend first with `curl`.

```bash
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Practice Flask"}'
```

On Windows PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/posts" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title": "Practice Flask"}'
```

Expected response:

```json
{
  "id": 4,
  "title": "Practice Flask",
  "done": false
}
```

## Add Dynamic Routes

Sometimes React needs one item by ID.

Add this route:

```python
@app.get("/api/posts/<int:post_id>")
def get_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            return jsonify(post)

    return jsonify({
        "error": "Post not found"
    }), 404
```

Now visit:

```text
http://127.0.0.1:5000/api/posts/1
```

## Explain Dynamic Routes

```python
@app.get("/api/posts/<int:post_id>")
```

This route has a variable part.

`<int:post_id>` means:

```text
Read this part of the URL as an integer.
```

So this URL:

```text
/api/posts/1
```

becomes:

```python
post_id = 1
```

```python
def get_post(post_id):
```

Flask passes the URL value into your function.

```python
for post in posts:
    if post["id"] == post_id:
        return jsonify(post)
```

This searches the list and returns the matching post.

```python
return jsonify({
    "error": "Post not found"
}), 404
```

If there is no match, return `404`.

Memorize:

```text
404 = the thing does not exist
```

## Add an Update Route

Use `PATCH` when React updates part of an existing item.

Add this route:

```python
@app.patch("/api/posts/<int:post_id>")
def update_post(post_id):
    data = request.get_json()

    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["done"] = data.get("done", post["done"])
            return jsonify(post)

    return jsonify({
        "error": "Post not found"
    }), 404
```

## Explain the Update Route

```python
@app.patch("/api/posts/<int:post_id>")
```

`PATCH` means:

```text
Update part of an existing resource.
```

```python
post["title"] = data.get("title", post["title"])
```

This means:

```text
Use the new title if React sent one.
Otherwise keep the old title.
```

Same idea here:

```python
post["done"] = data.get("done", post["done"])
```

This lets React update only one field at a time.

## Add a Delete Route

Use `DELETE` when React removes something.

Add this route:

```python
@app.delete("/api/posts/<int:post_id>")
def delete_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            return jsonify({
                "message": "Post deleted"
            })

    return jsonify({
        "error": "Post not found"
    }), 404
```

## Explain the Delete Route

```python
@app.delete("/api/posts/<int:post_id>")
```

This creates a DELETE route.

```python
posts.remove(post)
```

This removes the matching post from the list.

```python
return jsonify({
    "message": "Post deleted"
})
```

This confirms the delete worked.

Some APIs return no JSON and use status code `204`.

For learning, a message is easier to see.

## Complete Flask File

Here is the full `backend/app.py`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


posts = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Connect Flask to React", "done": False},
    {"id": 3, "title": "Build a full-stack app", "done": False},
]


@app.get("/")
def home():
    return jsonify({
        "message": "Flask API is running"
    })


@app.get("/api/posts")
def get_posts():
    return jsonify(posts)


@app.post("/api/posts")
def create_post():
    data = request.get_json()

    title = data.get("title")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "done": False
    }

    posts.append(new_post)

    return jsonify(new_post), 201


@app.get("/api/posts/<int:post_id>")
def get_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            return jsonify(post)

    return jsonify({
        "error": "Post not found"
    }), 404


@app.patch("/api/posts/<int:post_id>")
def update_post(post_id):
    data = request.get_json()

    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["done"] = data.get("done", post["done"])
            return jsonify(post)

    return jsonify({
        "error": "Post not found"
    }), 404


@app.delete("/api/posts/<int:post_id>")
def delete_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            return jsonify({
                "message": "Post deleted"
            })

    return jsonify({
        "error": "Post not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
```

## API Cheat Sheet

| Action | HTTP Method | Flask Route | Meaning |
| --- | --- | --- | --- |
| Read all posts | `GET` | `/api/posts` | Give React the list |
| Read one post | `GET` | `/api/posts/1` | Give React one item |
| Create post | `POST` | `/api/posts` | Add a new item |
| Update post | `PATCH` | `/api/posts/1` | Change part of an item |
| Delete post | `DELETE` | `/api/posts/1` | Remove an item |

## Status Code Cheat Sheet

| Code | Meaning | Use It When |
| --- | --- | --- |
| `200` | OK | A normal request worked |
| `201` | Created | A POST request created something |
| `400` | Bad Request | React sent invalid or missing data |
| `404` | Not Found | The requested item does not exist |
| `500` | Server Error | Flask crashed or something unexpected happened |

## Flask Patterns to Memorize

### Create the app

```python
app = Flask(__name__)
```

### Send JSON

```python
return jsonify({"message": "Hello"})
```

### Read JSON from React

```python
data = request.get_json()
```

### Make a GET route

```python
@app.get("/api/items")
def get_items():
    return jsonify(items)
```

### Make a POST route

```python
@app.post("/api/items")
def create_item():
    data = request.get_json()
    return jsonify(data), 201
```

### Make a route with an ID

```python
@app.get("/api/items/<int:item_id>")
def get_item(item_id):
    return jsonify({"id": item_id})
```

## Common Mistakes

### Forgetting CORS

If React cannot call Flask and the browser console mentions CORS, install and enable `flask-cors`:

```python
from flask_cors import CORS

CORS(app)
```

### Forgetting `jsonify`

Prefer this:

```python
return jsonify({"message": "Hello"})
```

Instead of this:

```python
return {"message": "Hello"}
```

Flask can return dictionaries directly in many cases, but `jsonify` makes your intention obvious while learning.

### Forgetting to Import `request`

If you use:

```python
request.get_json()
```

Then you must import it:

```python
from flask import request
```

### Expecting List Data to Persist

This tutorial stores data in a Python list.

That is fine for learning routes.

It is not a database.

When the server restarts, the list resets.

## The Mental Model

Memorize this:

```text
Route receives request.
Function runs.
Function returns response.
React uses the JSON.
```

And this:

```text
GET    = read
POST   = create
PATCH  = update
DELETE = remove
```

That is the core of Flask APIs for React.
