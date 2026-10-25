import os
from dotenv import load_dotenv

load_dotenv()  # reads .env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_PROFILE_PATH = os.path.join(BASE_DIR, "chrome_profile")  # used in whatsapp.py
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Every message the bot sends starts with this tag, and the bot ignores
# any message that starts with it. Keep it plain ASCII (no emoji).
BOT_PREFIX = "[Bot]"

# data.py
DATA_DIR = os.path.join(BASE_DIR, "data")
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule.json")
TODOS_FILE = os.path.join(DATA_DIR, "todos.json")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")

SEND_TIME = "07:30"  # 24-hour HH:MM