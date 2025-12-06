# Features to consider:
# Streaks
# Custom Task points

from flask import Flask, redirect, render_template, request, jsonify, g
from datetime import datetime
import sqlite3

app = Flask(__name__)

DATABASE = './productivity.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    try:
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Top part is all databse related, below is the actual app 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shallow")
def add_shallow():
    return ""

@app.route("/deep")
def add_deep():
    return ""

@app.route("/tdl")
def add_tdl():
    return ""

@app.route("/fetch_labels")
def fetch_labels():
    return ""

@app.route("/statistics")
def function ():
    return ""

@app.route("/history")
def function2 ():
    return ""

@app.route("/purchase")
def function3 ():
    return ""

@app.route("/settings")
def function4 ():
    return ""