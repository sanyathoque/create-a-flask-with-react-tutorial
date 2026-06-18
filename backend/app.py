from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


posts = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Connect Flask to React", "done": False},
    {"id": 3, "title": "Build a full-stack app", "done": False},
]


def find_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            return post

    return None


def next_post_id():
    if not posts:
        return 1

    return max(post["id"] for post in posts) + 1


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
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    new_post = {
        "id": next_post_id(),
        "title": title,
        "done": False
    }

    posts.append(new_post)

    return jsonify(new_post), 201


@app.get("/api/posts/<int:post_id>")
def get_post(post_id):
    post = find_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    return jsonify(post)


@app.patch("/api/posts/<int:post_id>")
def update_post(post_id):
    post = find_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    data = request.get_json(silent=True) or {}

    post["title"] = data.get("title", post["title"])
    post["done"] = data.get("done", post["done"])

    return jsonify(post)


@app.delete("/api/posts/<int:post_id>")
def delete_post(post_id):
    post = find_post(post_id)

    if not post:
        return jsonify({
            "error": "Post not found"
        }), 404

    posts.remove(post)

    return jsonify({
        "message": "Post deleted"
    })


if __name__ == "__main__":
    app.run(debug=True)
