from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://<JohnMiner>:<PlayL1st3r>@ds017688.mlab.com:17688/heroku_9ktnwzhl')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
playlists = db.playlists
comments = db.comments
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
    return render_template("playlists_new.html", playlist={}, title="New Playlist")


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    print(request.form.to_dict())
    playlist = {
        "title": request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'created_at': datetime.now()
    }
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template("playlists_show.html", playlist=playlist, comments=playlist_comments)


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist}
    )
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    video_links = '/n'.join(playlist.get('videos'))
    return render_template("playlists_edit.html", playlist=playlist, title="Edit Playlist", video_links=video_links)


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    playlists.delete_one({"_id": ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


@app.route('/playlists/comments', methods=['POST'])
def comment_new():
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=comment['playlist_id']))


@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    if request.form.get('_method') == 'DELETE':
        comment = comments.find_one({'_id': ObjectId(comment_id)})
        comments.delete_one({'_id': ObjectId(comment_id)})
        return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))
    else:
        raise NotFound()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    # app.run(debug=True)
