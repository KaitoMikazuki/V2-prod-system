from flask import current_app, g
import sqlite3

personal_db = './productivity.db'
debug_db = './debug.db'
DATABASE = debug_db

def get():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query(query, args=(), one=False):
    cur = get().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init():
    try:
        db = get()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())

        query("INSERT INTO state DEFAULT VALUES")
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

