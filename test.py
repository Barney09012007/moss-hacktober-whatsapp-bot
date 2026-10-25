import time
from whatsapp import open_whatsapp, read_messages

driver = open_whatsapp()
time.sleep(3)  # let the chat finish loading

seen_count = len(read_messages(driver))
print(f"Snapshot: ignoring {seen_count} old messages. Send a reply from your main phone now.")

try:
    while True:
        current = read_messages(driver)
        new = current[seen_count:]
        for msg in new:
            print("NEW:", msg)
        seen_count = len(current)
        time.sleep(3)
except KeyboardInterrupt:
    print("stopped")