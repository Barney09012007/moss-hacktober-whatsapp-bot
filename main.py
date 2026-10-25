import time
from whatsapp import open_whatsapp, send_message, read_messages
from ai import interpret_reply
from actions import apply_actions
from data import get_open_todos

def handle(driver, text):
    try:
        actions = interpret_reply(text)
    except Exception as e:
        print("AI error:", e)
        return
    if not actions:
        return  # not a todo command, stay quiet
    results = apply_actions(actions)
    if results:
        remaining = len(get_open_todos())
        send_message(driver, "\n".join(results) + f"\n\nStill open: {remaining}")

def main():
    driver = open_whatsapp()
    time.sleep(3)
    seen_count = len(read_messages(driver))
    print(f"Listening. Ignoring {seen_count} old messages.")

    while True:
        try:
            current = read_messages(driver)
            for msg in current[seen_count:]:
                print("NEW:", msg)
                handle(driver, msg)
            seen_count = len(current)
        except Exception as e:
            print("Loop error:", e)
        time.sleep(3)

if __name__ == "__main__":
    main()