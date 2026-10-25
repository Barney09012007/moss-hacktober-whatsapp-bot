import os
from dotenv import load_dotenv
load_dotenv() #reading env file

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
CHROME_PROFILE_PATH=os.path.join(BASE_DIR,"chrome_profile") #line 16 whatsapp.py
PHONE_NUMBER=os.getenv("PHONE_NUMBER")
BOT_NAME=os.getenv("BOT_NAME")


#data.py 
DATA_DIR=os.path.join(BASE_DIR,"data")
SCHD_DIR=os.path.join(DATA_DIR,"schd.json")
TODOS_DIR=os.path.join(DATA_DIR,"todos.json")

SEND_TIME="7:30"