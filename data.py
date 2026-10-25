import json
from datetime import datetime
from config import SCHEDULE_FILE, TODOS_FILE

def get_todays_classes():
    with open(SCHEDULE_FILE) as f:
        schedule = json.load(f)
    today = datetime.now().strftime("%A").lower()
    return schedule.get(today, [])

def _load_todos():
    with open(TODOS_FILE) as f:
        return json.load(f)

def _save_todos(todos):
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def get_open_todos():
    return [t for t in _load_todos() if not t["done"]]

def mark_todo_done(task_name):
    todos = _load_todos()
    found = False
    for t in todos:
        if t["task"].lower() == task_name.lower():
            t["done"] = True
            found = True
    _save_todos(todos)
    return found

def add_todo(task_name):
    todos = _load_todos()
    todos.append({"task": task_name, "done": False})
    _save_todos(todos)

def remove_todo(task_name):
    todos = _load_todos()
    kept = [t for t in todos if t["task"].lower() != task_name.lower()]
    _save_todos(kept)
    return len(kept) != len(todos)