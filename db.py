from flask import current_app, g
import sqlite3
from decimal import Decimal
from models import Filters

personal_db = './productivity.db'
debug_db = './debug.db'
DATABASE = personal_db

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

def secs_to_mins(seconds) -> Decimal:
    return Decimal(seconds)/60 

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
    # TODO: Handle the case where the user wants to change task values
    add_points = data["points"]
    query("UPDATE state SET current_points = current_points + ?", (add_points,))

def reset_state():
    query("DELETE FROM state;")
    query("INSERT INTO state DEFAULT VALUES;")
    get().commit()

def calculate_points(conditions:Filters):
    data = build_query(conditions, execute=True)
    total_points = 0
    for row in data:
        total_points += int(row["points"])
    return to_decimal(total_points)

def calculate_time(conditions:Filters) -> int | Decimal :
    data = build_query(conditions, execute=True)
    total_minutes = 0
    for row in data:
        if not row["work_type"] in ('shallow', 'deep'):
            continue
        total_minutes += row["minutes"]
        total_minutes += secs_to_mins(row["seconds"])
    return total_minutes

def calculate_total_tdl(conditions: Filters):
    data = build_query(conditions, execute=True)
    print(data[0])
    total_tdl = 0
    for _ in range(len(data)):
        total_tdl += 1
    return total_tdl

# TODO:
def view_logs(conditions:Filters):
    return ""

# TODO:
def statistics(conditions:Filters):
    return ""

# Builds the query with 2 internal helper functions, 
def build_query(conditions: Filters, execute=False) -> dict: 
    args = []

    filters = [build_typecondition("work_type", args, conditions), build_typecondition("label", args, conditions),
    build_dateconditions(conditions.start_date, conditions.end_date,args)]

    where_clause = []
    for i in filters: 
        if i:
            where_clause.append(i)

    where_clause = "AND ".join(where_clause)

    if execute:
        data = query(f"SELECT {conditions.datacolumn} FROM logs WHERE {where_clause}", args)
        return data
    else:
        sql_query = {
            "sql":f"SELECT {conditions.datacolumn} FROM logs",
            "where_clause": f"WHERE {where_clause}",
            "args": args,
        }
        return sql_query

# for work_type and label conditions in the where_clause
def build_typecondition(column_name, args:list, conditions: Filters): 
    condition = getattr(conditions, column_name)
    if condition == (): # () means any value, if so, omit the condition
        return ""
    if condition == (None,):   # (None,) means the user explicitly searches Null 
        return f"{column_name} IS NULL "
    search_null = False
    placeholders = []
    for i in condition:
        if i is None:
            search_null = True
            continue
        placeholders.append("?")
        args.append(i)
    querycondition = f"{column_name} IN ({', '.join(placeholders)}) "
    if search_null is True:
        querycondition += f"OR {column_name} IS NULL "
    return querycondition

# For start_date and end_date conditions in the where clause
def build_dateconditions(start_date, end_date, args:list):
    conditions = []
    if start_date:
        conditions.append("logged_at >= ? ")
        args.append(start_date)
    if end_date:
        conditions.append("logged_at <= ?")
        args.append(end_date)
    return "AND ".join(conditions)
