from flask import current_app, g
import sqlite3
from decimal import Decimal
from models import Filters

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


def handle_datarequest(request_type, filters:Filters):
    match request_type:
        case "calculate_points":
            statement = build_query(filters)
            data = query(statement[0], statement[1])
            total_points = 0
            for row in data:
                total_points += int(row["points"])
            return to_decimal(total_points)
                
        case "calculate_time":
            statement = build_query(filters)
            data = query(statement[0], statement[1])
            total_minutes = 0
            for row in data:
                if not row["work_type"] in ('shallow', 'deep'):
                    continue
                total_minutes += row["minutes"]
                total_minutes += secs_to_mins(row["seconds"])
            return total_minutes
        
        case "calculate_total_tdl":
            statement = build_query(filters)
            data = query(statement[0], statement[1])
            total_tdl = 0
            # TODO: What is the return type of data? len() is o(1) only for list tuples and strs because they are internally stored 
            for _ in data:
                total_tdl += 1
            return total_tdl
            
        case "view_logs":
            # TODO:
            return ""
        
        case "statistics":
            # TODO:
            return ""

# Builds the query with 2 internal helper functions, returns a tuple with the query and the args
def build_query(filters: Filters) -> tuple: 
    args = []
    def build_typeconditions(column_name): # For work_type and label conditions
        conditions = getattr(filters, column_name)

        if conditions == (): # () means any value, if so, omit the condition
            return ""
        if conditions == (None,):   # (None,) means the user explicitly searches Null 
            return f"{column_name} IS NULL "
    
        # Dynamically identifies conditions
        search_null = False
        placeholders = []
        for i in conditions:
            if i is None:
                search_null = True
                continue
            placeholders.append("?")
            args.append(i)
        querycondition = f"{column_name} IN ({', '.join(placeholders)}) "
        if search_null is True:
            querycondition += f"OR {column_name} IS NULL "

        return querycondition

    # For start_date and end_date conditions
    def build_dateconditions(start_date, end_date):
        conditions = []

        if start_date:
            conditions.append("logged_at >= ? ")
            args.append(start_date)
        if end_date:
            conditions.append("logged_at <= ?")
            args.append(end_date)
     
        return "AND ".join(conditions)

    conditions = [build_typeconditions("work_type"), build_typeconditions("label"),build_dateconditions(filters.start_date, filters.end_date)]

    where_clause = []
    for i in conditions: 
        if i:
            where_clause.append(i)

    where_clause = "AND ".join(where_clause)

    querystatement = (f"SELECT * FROM logs WHERE {where_clause}", args )
    return querystatement