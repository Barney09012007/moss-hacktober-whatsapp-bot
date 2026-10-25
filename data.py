import os
import json
from datetime import datetime
from config import DATA_DIR, SCHEDULE_FILE, TODOS_FILE, REMINDERS_FILE


def _ensure_files():
    """Create the data folder and empty JSON files if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    defaults = {SCHEDULE_FILE: {}, TODOS_FILE: [], REMINDERS_FILE: []}
    for path, default in defaults.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default, f, indent=2)


_ensure_files()


def get_todays_classes():
    with open(SCHEDULE_FILE) as f:
        schedule = json.load(f)
    today = datetime.now().strftime("%A").lower()
    return schedule.get(today, [])


# ---------- todos ----------

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
        if t["task"].lower() == task_name.lower() and not t["done"]:
            t["done"] = True
            found = True
    if found:
        _save_todos(todos)
    return found


def add_todo(task_name):
    todos = _load_todos()
    todos.append({"task": task_name, "done": False})
    _save_todos(todos)


def remove_todo(task_name):
    todos = _load_todos()
    kept = [t for t in todos if t["task"].lower() != task_name.lower()]
    if len(kept) != len(todos):
        _save_todos(kept)
        return True
    return False


# ---------- reminders ----------

def _load_reminders():
    with open(REMINDERS_FILE) as f:
        return json.load(f)


def _save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)


def add_reminder(task, when_str):
    reminders = _load_reminders()
    reminders.append({"task": task, "when": when_str, "sent": False})
    _save_reminders(reminders)


def get_due_reminders():
    """Returns [(index, task)] for reminders whose time has come.

    Does NOT mark them sent. Call mark_reminder_sent(index) after the
    WhatsApp message has actually gone out, so a failed send is retried.
    """
    now = datetime.now()
    due = []
    for i, r in enumerate(_load_reminders()):
        if r.get("sent"):
            continue
        try:
            when = datetime.strptime(r["when"], "%Y-%m-%d %H:%M")
        except (KeyError, ValueError):
            continue  # skip a malformed entry instead of breaking the loop
        if when <= now:
            due.append((i, r["task"]))
    return due


def mark_reminder_sent(index):
    reminders = _load_reminders()
    if 0 <= index < len(reminders):
        reminders[index]["sent"] = True
        _save_reminders(reminders)