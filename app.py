# Features to consider:
# Streaks
# Custom Task points
# Disappear once it reaches the nav 
# Log reasons for failing to log a focus session

# Bugs:
# Safari linear gradient body bg
# Dynamic sizing for the navbar and index

from flask import Flask, redirect, render_template, request, jsonify, g
from datetime import datetime
import sqlite3
from helpers import validate_form_data, now

app = Flask(__name__)
# ===== AUTO-REFRESH CONFIG (START - REMOVE THIS SECTION) =====
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['ENV'] = 'development'
# ===== AUTO-REFRESH CONFIG (END) =====

personal_db = './productivity.db'
debug_db = './debug.db'
DATABASE = debug_db

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
            query_db("INSERT INTO state DEFAULT VALUES")
            db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    # TODO: Initialize state table

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shallow", methods=['POST'])
def add_shallow():
    # TODO(PURCHASE&SETTINGS): Interact with state properly
    # TODO: Accomodate points
    work_type = "shallow"
    data = request.form.to_dict()
    data = validate_form_data(data) 
    if data != False:
        query_db("INSERT INTO logs (work_type, minutes, seconds, logged_at, label, notes) VALUES (?, ?, ?, ?, ?, ?)", (work_type, data['minutes'], data['seconds'], now(), data['label'], data['notes']))
        get_db().commit()
        # TODO: Tell user that the log operation was successful
    # else: 
        # TODO: RETURN ERROR - Warn user that input is wrong
    return redirect("/")

@app.route("/deep", methods=["POST"])
def add_deep():
    # TODO(PURCHASE&SETTINGS): Interact with state properly
    # TODO: Accomodate points
    work_type = "deep"
    data = request.form.to_dict()
    data = validate_form_data(data) 
    if data != False:
        query_db("INSERT INTO logs (work_type, minutes, seconds, logged_at, label, notes) VALUES (?, ?, ?, ?, ?, ?)", (work_type, data['minutes'], data['seconds'], now(), data['label'], data['notes']))
        get_db().commit()
        # TODO: Tell user that the log operation was successful
    # else: 
        # TODO: RETURN ERROR - Warn user that input is wrong
    return redirect("/")


@app.route("/tdl")
def add_tdl():
    # TODO: This involves JS to log the tdl 
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


# # ============================================================
# # AUTO-REFRESH BROWSER - DELETE THIS ENTIRE SECTION BLOCK
# # ============================================================
# @app.after_request
# def add_live_reload(response):
#     """Injects a live reload script into HTML responses in development mode"""
#     if app.debug and response.content_type and 'text/html' in response.content_type:
#         live_reload_script = """
#         <script>
#         (function() {
#             setInterval(function() {
#                 fetch(window.location.href)
#                     .then(r => r.text())
#                     .then(html => {
#                         if (html !== document.documentElement.outerHTML) {
#                             location.reload();
#                         }
#                     })
#                     .catch(e => {});
#             }, 200000);
#         })();
#         </script>
#         """
#         if response.data:
#             body = response.data.decode('utf-8')
#             if '</body>' in body:
#                 body = body.replace('</body>', live_reload_script + '</body>')
#                 response.set_data(body)
#     return response
# # ============================================================
# # END OF AUTO-REFRESH BROWSER SECTION
# # ============================================================


if __name__ == '__main__':
    app.run(debug=True)