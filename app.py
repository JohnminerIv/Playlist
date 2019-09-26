from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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


@app.route('/playlists/new')
def playlists_new():
    return render_template("playlists_new.html")


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    print(request.form.to_dict())
    playlist = {
        "title": request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlist/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template("playlists_show.html", playlist=playlist)


if __name__ == '__main__':
    app.run(debug=True)
