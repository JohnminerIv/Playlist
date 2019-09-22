from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists
app = Flask(__name__)
"""
playlists = [
    {"title": "cat videos", "description": "cats acting weird"},
    {"title": "workout playlist", "description": "Get pumped!"}
]


@app.route('/')
def index():
    # Return homepage.
    return render_template("home.html", message="flask is cool")
"""


@app.route('/')
def playlists_index():
    """Return playlists."""
    return render_template("playlists_index.html", playlists=playlists.find())


if __name__ == '__main__':
    app.run(debug=True)
