# Features to consider:
# Streaks
# Custom Task points
# Disappear once it reaches the nav 
# Log reasons for failing to log a focus session

# Bugs:
# Safari linear gradient body bg
# Dynamic sizing for the navbar and index

# TODO:
# Manual deduct - User should determine whether it would deduct from tdl deep or shallow or adjusting or None, We'll do this using negative values, label of adjusting_entry

from flask import Flask, redirect, render_template, request, jsonify, g
from datetime import datetime
from helpers import validate_form_data, now, calculate_pointval
from models import Filters
import db

            

def create_app():
    app = Flask(__name__)
    @app.teardown_appcontext #This will run for every request
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    return app

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    db.init()
    print("Database initialized.")

@app.cli.command("reset-state")
def reset_state_command():
    db.reset_state()
    print("State has been reset.")
    

# ===== AUTO-REFRESH CONFIG (START - REMOVE THIS SECTION) =====
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['ENV'] = 'development'
# ===== AUTO-REFRESH CONFIG (END) =====


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shallow", methods=['POST'])
def add_shallow():
    data = request.form.to_dict()
    data["work_type"] = "shallow" 
    data['logged_at'] = now()
    data = validate_form_data(data) 
    
    if data != False:
        data["points"] = calculate_pointval(data) 
        db.query("INSERT INTO logs (work_type, minutes, seconds, logged_at, points, label, notes) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["work_type"], data['minutes'], data['seconds'], data['logged_at'], data['points'], data['label'], data['notes']))
        db.update_state(data)
        db.get().commit()
        # TODO: Tell user that the log operation was successful
    # else: 
        # TODO: RETURN ERROR - Warn user that input is wrong
    return redirect("/")

@app.route("/deep", methods=["POST"])
def add_deep():
    data = request.form.to_dict()
    data["work_type"] = "deep" #Don't modify
    data['logged_at'] = now()
    data = validate_form_data(data) 
    if data != False:
        data["points"] = calculate_pointval(data)
        db.query("INSERT INTO logs (work_type, minutes, seconds, logged_at, points, label, notes) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["work_type"], data['minutes'], data['seconds'], data['logged_at'], data['points'], data['label'], data['notes']))
        db.update_state(data)
        db.get().commit()
        # TODO: Tell user that the log operation was successful
    # else: 
        # TODO: RETURN ERROR - Warn user that input is wrong
    return redirect("/")


@app.route("/tdl", methods=["POST"])
def add_tdl():
    # TODO: Integrate the dynamic totals computation 
    data = {
        "work_type": "tdl",
        "logged_at": now(),
    }
    data["points"] = calculate_pointval(data)
    db.query("INSERT INTO logs (work_type, logged_at, points) VALUES (?, ?, ?)", (data["work_type"], data["logged_at"], data["points"]))
    db.update_state(data)
    db.get().commit()
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


# API REQUESTS
@app.route("/pass_totaltdl", methods=["GET"])
def pass_totaltdl():
    conditions = Filters(work_type=('tdl',)) 
    total_tdl = db.calculate_total_tdl(conditions)
    return {"total_tdl": total_tdl}

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