from flask import request
from datetime import datetime
import db
import plotly.express as px
from decimal import Decimal
from models import Filters

def validate_form_data(data=dict):
    # TODO: Handle cases where the user removes sections using Devtools, 
    if not isinstance(data, dict):
        raise TypeError

    # If user did not provide inputs, set default values
    data.setdefault("label", None)
    if data["notes"] == "":
        data["notes"] = None
    if data['seconds'] == "":
        data['seconds'] = 0

    try:
        minutes = int(data['minutes'])
        seconds = int(data['seconds'])
    except ValueError:
        return False
    if minutes < 0 or seconds < 0:
        return False
    if minutes == 0 and seconds == 0:
        return False

    if data['notes'] != None and len(data['notes']) > 400:
        return False
    
    return data

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def calculate_pointval(data=dict):
    if data["work_type"] == 'tdl': # pyright: ignore[reportUndefinedVariable]
        return db.query("SELECT tdl_value FROM state", one=True)["tdl_value"]
    else:
        pointval = db.get_pointval(data["work_type"])  # pyright: ignore[reportUndefinedVariable]
        points = 0
        points += int(data["minutes"]) * pointval # pyright: ignore[reportUndefinedVariable]
        points += db.secs_to_mins(data["seconds"]) * pointval # pyright: ignore[reportUndefinedVariable]
        return int(db.to_scaled(points))

def get_period_preference():
     period_pref = db.query("SELECT period_start, period_end FROM state")
     return period_pref

def create_productivitygraph(df):
    fig = px.bar(df,
        x="day",
        y = "total_minutes",
        color="work_type",
        barmode="stack", 
        labels = dict(day="Date", total_minutes="Total minutes", work_type="Work Type"),
        )

    fig.update_layout(
        bargap=0.4,
        legend_title_text = "Work Type",
        hovermode = "x unified"
    )

    fig.update_traces(
        hovertemplate = "%{y} minutes"
    )
    return fig

def build_dialogFormQuery(dialogInput=None) -> dict:
    filters = Filters()
    state = db.query("SELECT period_start, period_end FROM state")[0]

    if state["period_start"]:
        filters.start_date = state["period_start"]
    if state["period_end"]:
        filters.end_date = state["period_end"]

    query_parts = db.build_query(filters)
    where_clause = query_parts["where_clause"]
    args_clause = query_parts["args"]

    dialogQuery = f'''
    SELECT
        DATE(logged_at) AS day,
        SUM(minutes) AS total_minutes,
        SUM(seconds) AS total_seconds,
        work_type,
        label
    FROM logs
    {where_clause}
    GROUP BY DATE(logged_at), work_type
    ORDER BY day;
    '''
    return {"sql":dialogQuery, "args": args_clause}