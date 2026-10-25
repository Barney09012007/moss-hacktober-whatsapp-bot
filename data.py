import json
from datetime import datetime
from config import SCHEDULE_FILE, TODOS_FILE

def get_todays_classes():
    with open(SCHEDULE_FILE) as f:
        schedule = json.load(f)
    today = datetime.now().strftime("%A").lower()
    return schedule.get(today, [])

def get_open_todos():
    with open(TODOS_FILE) as f:
        todos = json.load(f)
    return [t for t in todos if not t["done"]]

def mark_todo_done(task_name):
    with open(TODOS_FILE) as f:
        todos = json.load(f)
    for t in todos:
        if t["task"].lower() == task_name.lower():
            t["done"] = True
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)