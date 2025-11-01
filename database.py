import sqlite3
import os

DB_FILE = 'mental_health.db'

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Ensure DB directory exists (not necessary here but safe)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mood TEXT,
        notes TEXT,
        date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT,
        date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS forum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        body TEXT,
        date TEXT
    )
    ''')

    # New: articles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        summary TEXT,
        content TEXT,
        source_url TEXT,
        date TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# MOODS
def insert_mood(mood, notes, date):
    conn = get_connection()
    conn.execute('INSERT INTO moods (mood, notes, date) VALUES (?, ?, ?)', (mood, notes, date))
    conn.commit()
    conn.close()

def get_moods():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM moods ORDER BY date DESC').fetchall()
    conn.close()
    return rows

# JOURNALS
def insert_journal(entry, date):
    conn = get_connection()
    conn.execute('INSERT INTO journals (entry, date) VALUES (?, ?)', (entry, date))
    conn.commit()
    conn.close()

def get_journals():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM journals ORDER BY date DESC').fetchall()
    conn.close()
    return rows

# FORUM
def insert_post(title, body, date):
    conn = get_connection()
    conn.execute('INSERT INTO forum (title, body, date) VALUES (?, ?, ?)', (title, body, date))
    conn.commit()
    conn.close()

def get_posts():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM forum ORDER BY date DESC').fetchall()
    conn.close()
    return rows

# ARTICLES (new)
def insert_article(title, summary, content, source_url, date):
    conn = get_connection()
    conn.execute(
        'INSERT INTO articles (title, summary, content, source_url, date) VALUES (?, ?, ?, ?, ?)',
        (title, summary, content, source_url, date)
    )
    conn.commit()
    conn.close()

def get_articles():
    conn = get_connection()
    rows = conn.execute('SELECT * FROM articles ORDER BY date DESC').fetchall()
    conn.close()
    return rows
