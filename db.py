from flask import current_app, g
import sqlite3
from decimal import Decimal

personal_db = './productivity.db'
debug_db = './debug.db'
DATABASE = debug_db

def get():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.set_trace_callback(lambda q: print(f"\033[92m{q}\033[0m")) #Prints the sql query and with a different color
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

# Helpers
def to_decimal(scaled: int): 
    return Decimal(scaled)/ 100

def to_scaled(value: Decimal) -> int:
    return int(Decimal(value) * 100)

def get_pointval(work_type):
    pointvals = query("SELECT deep_value, shallow_value, tdl_value FROM state", one=True)
    match work_type:
        case "shallow":
            return to_decimal(pointvals["shallow_value"])
        case "deep":
            return to_decimal(pointvals["deep_value"])
        case "tdl":
            return to_decimal(pointvals["tdl"])
    return KeyError

def update_state(data):
    add_points = data["points"]
    if (data["work_type"] == 'tdl'):
        query("UPDATE state SET total_deep = total_tdl + ?, current_points = current_points + ?, total_points = total_points + ?", (add_points, add_points, add_points))
        return
    add_minutes = to_scaled(int(data["minutes"]) + Decimal(data["seconds"])/60) #converts seconds to minute format, then adds
    match data["work_type"]: # Only differs in first column
        case "shallow":
            query("UPDATE state SET total_shallow = total_shallow + ?,current_points = current_points + ?, total_points = total_points + ?", (add_minutes, add_points, add_points))
        case "deep":
            query("UPDATE state SET total_deep = total_deep + ?, current_points = current_points + ?, total_points = total_points + ?", (add_minutes, add_points, add_points))

    

def reset_state():
    query("DELETE FROM state;")
    query("INSERT INTO state DEFAULT VALUES;")
    get().commit()