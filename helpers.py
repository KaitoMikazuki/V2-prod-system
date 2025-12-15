from flask import request
from datetime import datetime
import db
from decimal import Decimal

def validate_form_data(data=dict):
    # TODO: Handle cases where the user removes sections using Devtools, 
    if not isinstance(data, dict):
        return TypeError

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
    if data["work_type"] == 'tdl':
        return db.query("SELECT tdl_value FROM state", one=True)["tdl_value"]
    else:
        pointval = db.get_pointval(data["work_type"])
        points = 0
        points += int(data["minutes"]) * pointval
        points += Decimal(data["seconds"])/60 * pointval
        return int(db.to_scaled(points))


