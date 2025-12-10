from flask import request

def validate_form_data(data=dict):
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
    if minutes < 0:
        return False
    if seconds < 0: 
        return False
    
    if data['notes'] != None and len(data['notes']) > 400:
        return False
    
    return data

    

# sqlite3 queries