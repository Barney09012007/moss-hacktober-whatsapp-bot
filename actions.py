from datetime import datetime
from data import get_open_todos, mark_todo_done, add_todo, remove_todo, add_reminder

def apply_actions(actions):
    results = []
    open_tasks = {t["task"].lower(): t["task"] for t in get_open_todos()}

    for a in actions:
        kind = a.get("type")
        task = (a.get("task") or "").strip()
        if not task:
            continue

        if kind == "done":
            if task.lower() in open_tasks and mark_todo_done(task):
                results.append(f"Done: {open_tasks[task.lower()]}")
            else:
                results.append(f"Couldn't find: {task}")
        elif kind == "add":
            add_todo(task)
            results.append(f"Added: {task}")
        elif kind == "remove":
            if remove_todo(task):
                results.append(f"Removed: {task}")
            else:
                results.append(f"Couldn't find: {task}")
        elif kind == "remind":
            when = (a.get("time") or "").strip()
            try:
                dt = datetime.strptime(when, "%Y-%m-%d %H:%M")
            except ValueError:
                results.append(f"Couldn't understand the time for: {task}")
                continue
            if dt <= datetime.now():
                results.append(f"That time has already passed: {task}")
                continue
            add_reminder(task, when)
            results.append(f"Reminder set: {task} at {dt.strftime('%I:%M %p, %d %b')}")

    return results