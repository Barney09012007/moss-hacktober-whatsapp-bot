import time
from datetime import datetime
from config import SEND_TIME
from whatsapp import open_whatsapp, send_message, read_messages_with_ids
from ai import interpret_reply
from actions import apply_actions
from data import get_open_todos, pop_due_reminders
from message import build_morning_message

def send_hm():
    h, m = SEND_TIME.split(":")
    return int(h), int(m)

def handle(driver, text):
    try:
        actions, reply = interpret_reply(text)
    except Exception as e:
        print("AI error:", e)
        send_message(driver, "AI hiccup, check the terminal.")
        return
    lines = apply_actions(actions) if actions else []
    if any(l.startswith(("Done", "Added", "Removed")) for l in lines):
        lines.append(f"\nStill open: {len(get_open_todos())}")
    if reply:
        lines.append(reply)
    if lines:
        send_message(driver, "\n".join(lines))

def main():
    driver = open_whatsapp()
    time.sleep(3)
    first = read_messages_with_ids(driver)
    seen_ids = {mid for mid, _ in first}
    print(f"Listening. Ignoring {len(first)} old messages. Morning message at {SEND_TIME}.")
    if first:
        print("Sample id:", first[-1][0])

    now = datetime.now()
    # if we start after today's send time, don't send a late morning message
    last_morning = now.date() if (now.hour, now.minute) >= send_hm() else None

    while True:
        try:
            for mid, text in read_messages_with_ids(driver):
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                print("NEW:", text)
                handle(driver, text)

            for task in pop_due_reminders():
                send_message(driver, f"Reminder: {task}")

            now = datetime.now()
            if last_morning != now.date() and (now.hour, now.minute) >= send_hm():
                send_message(driver, build_morning_message())
                last_morning = now.date()
        except Exception as e:
            print("Loop error:", e)
        time.sleep(3)

if __name__ == "__main__":
    main()