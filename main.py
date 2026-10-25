import time
from datetime import datetime
from config import SEND_TIME
from whatsapp import open_whatsapp, send_message, read_messages_with_ids
from ai import interpret_reply
from actions import apply_actions
from data import get_open_todos, get_due_reminders, mark_reminder_sent
from message import build_morning_message


def send_hm():
    t = datetime.strptime(SEND_TIME, "%H:%M")
    return t.hour, t.minute


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


BURST_LIMIT = 5  # more new messages than this in one poll = chat history loading, not real messages


def wait_for_history(driver, quiet_polls=3, max_wait=45):
    """Wait until the chat has finished loading, i.e. the message list stops changing.

    The message box appears before WhatsApp renders the history, so a fixed sleep
    can snapshot a half-loaded chat and later treat old messages as new ones.
    """
    last = None
    stable = 0
    deadline = time.time() + max_wait
    msgs = []
    while time.time() < deadline:
        msgs = read_messages_with_ids(driver)
        ids = {mid for mid, _ in msgs}
        if ids == last:
            stable += 1
            if stable >= quiet_polls:
                break
        else:
            stable = 0
            last = ids
        time.sleep(1)
    return msgs


def main():
    driver = open_whatsapp()
    first = wait_for_history(driver)
    seen_ids = {mid for mid, _ in first}
    print(f"Listening. Ignoring {len(first)} old messages. Morning message at {SEND_TIME}.")
    if first:
        print("Sample id:", first[-1][0])

    now = datetime.now()
    # if we start after today's send time, don't send a late morning message
    last_morning = now.date() if (now.hour, now.minute) >= send_hm() else None

    while True:
        try:
            new = [(mid, text) for mid, text in read_messages_with_ids(driver)
                   if mid not in seen_ids]
            if len(new) > BURST_LIMIT:
                # looks like old history rendering late (or scrolled in), not real new messages
                print(f"Skipping {len(new)} messages that appeared at once (assumed old history).")
                seen_ids.update(mid for mid, _ in new)
                new = []
            for mid, text in new:
                seen_ids.add(mid)
                print("NEW:", text)
                handle(driver, text)

            # mark a reminder sent only after the message actually went out
            for idx, task in get_due_reminders():
                send_message(driver, f"Reminder: {task}")
                mark_reminder_sent(idx)

            now = datetime.now()
            if last_morning != now.date() and (now.hour, now.minute) >= send_hm():
                send_message(driver, build_morning_message())
                last_morning = now.date()
        except Exception as e:
            print("Loop error:", e)
        time.sleep(3)


if __name__ == "__main__":
    main()