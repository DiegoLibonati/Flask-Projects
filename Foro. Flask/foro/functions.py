from datetime import datetime

def get_time_login():
    now = datetime.now()

    current_time = f"{add_zero(now.hour)}:{add_zero(now.minute)}:{add_zero(now.second)} | {add_zero(now.day)}/{add_zero(now.month)}/{now.year}"

    return current_time

def add_zero(value):

    if value < 10:
        return f"0{value}"
    
    return value