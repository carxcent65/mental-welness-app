from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from database import init_db, insert_mood, get_moods, insert_journal, get_journals, insert_post, get_posts, insert_article, get_articles
import os

# Frontend folder is in same directory
app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# Initialize DB
init_db()

# ---- Frontend serving ----
@app.route('/')
def serve_home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# ---- API endpoints ----

# Mood endpoints
@app.route('/add_mood', methods=['POST'])
def add_mood():
    data = request.get_json()
    if not data or 'mood' not in data:
        return jsonify({'error': 'mood required'}), 400
    mood = data['mood']
    notes = data.get('notes', '')
    date = datetime.now().strftime('%Y-%m-%d')
    insert_mood(mood, notes, date)
    return jsonify({'message': 'Mood added'})

@app.route('/get_moods', methods=['GET'])
def get_all_moods():
    rows = get_moods()
    return jsonify([dict(row) for row in rows])

# Journal endpoints
@app.route('/add_journal', methods=['POST'])
def add_journal():
    data = request.get_json()
    if not data or 'entry' not in data:
        return jsonify({'error': 'entry required'}), 400
    entry = data['entry']
    date = datetime.now().strftime('%Y-%m-%d')
    insert_journal(entry, date)
    return jsonify({'message': 'Journal added'})

@app.route('/get_journals', methods=['GET'])
def get_all_journals():
    rows = get_journals()
    return jsonify([dict(row) for row in rows])

# Forum endpoints
@app.route('/add_post', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or 'title' not in data or 'body' not in data:
        return jsonify({'error': 'title and body required'}), 400
    title = data['title']
    body = data['body']
    date = datetime.now().strftime('%Y-%m-%d')
    insert_post(title, body, date)
    return jsonify({'message': 'Post added'})

@app.route('/get_posts', methods=['GET'])
def get_all_posts():
    rows = get_posts()
    return jsonify([dict(row) for row in rows])

# ----- ARTICLES endpoints (new) -----
@app.route('/add_article', methods=['POST'])
def add_article_route():
    data = request.get_json()
    required = ['title']
    if not data or any(k not in data for k in required):
        return jsonify({'error': 'title required'}), 400
    title = data['title']
    summary = data.get('summary', '')
    content = data.get('content', '')
    source_url = data.get('source_url', '')
    date = datetime.now().strftime('%Y-%m-%d')
    insert_article(title, summary, content, source_url, date)
    return jsonify({'message': 'Article added'})

@app.route('/get_articles', methods=['GET'])
def get_all_articles():
    rows = get_articles()
    return jsonify([dict(row) for row in rows])

# ---- Run ----
if __name__ == '__main__':
    if not os.path.exists(app.static_folder):
        print(f"⚠️ Frontend folder not found: {app.static_folder}")
    else:
        print(f"✅ Serving frontend from: {app.static_folder}")
    print("🚀 Starting Flask server...")
    app.run(debug=True)
