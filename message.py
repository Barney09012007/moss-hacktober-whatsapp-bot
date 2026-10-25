from data import get_todays_classes, get_open_todos

def build_morning_message():
    classes = get_todays_classes()
    todos = get_open_todos()

    lines = ["Good morning!", ""]

    if classes:
        lines.append("Classes today:")
        for c in classes:
            lines.append(f"- {c['time']}  {c['subject']} {c.get('activity', '')}".rstrip())
    else:
        lines.append("No classes today.")

    lines.append("")
    if todos:
        lines.append("Your goals:")
        for t in todos:
            lines.append(f"- {t['task']}")
    else:
        lines.append("No goals set. Add some tonight.")

    return "\n".join(lines)

if __name__ == "__main__":
    print(build_morning_message())