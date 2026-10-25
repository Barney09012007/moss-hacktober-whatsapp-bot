# Whatsapp schedule and task bot  
Reads recent messages sent on any whatsapp chat, and manages tasks and schedules.  
You can set up To-do lists, reminders and functions as a general chat bot.  
Works when messaging yourself, or on other numbers and group chats.

## Requirements
Uses the selenium library, installed with: __pip install selenium python-dotenv google-genai__  
.env file to house your own API and phone number that starts with the country code(Should not be shared with anyone).  
Example .env format:  
__GEMINI_API_KEY=your_key__  
__MODEL_NAME=model name__  
__PHONE_NUMBER=911234567890__  
Requires Python 3.10 and Google chrome. 

## How to run it
Open a virtual environment in terminal using: source venv/bin/activate (Recommended to download setup in venv)
Generate an API Key through Google AI Studio (Please do not leak your API Keys)
Make sure you have the selenium library installed
Run python main.py
Script can be stopped by entering ctrl+c on the terminal


## Built with
Gemma 4  
Selenium (Python library)  
Whatsapp web  
Anthropic Claude to help write code and debug

# License  
Released under MIT license
