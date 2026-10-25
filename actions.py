from data import get_open_todos, mark_todo_done, add_todo, remove_todo

def apply_actions(actions):
    """Runs the AI's suggested actions. Returns a list of result lines."""
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

    return results