import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from data import get_open_todos
from prompt import PROMPT

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME")


def interpret_reply(text):
    todos = [t["task"] for t in get_open_todos()]
    now = datetime.now().strftime("%A, %Y-%m-%d %H:%M")
    prompt = (PROMPT.replace("{{NOW}}", now)
                    .replace("{{TODOS}}", json.dumps(todos))
                    .replace("{{MESSAGE}}", text))
    response = client.models.generate_content(model=MODEL, contents=prompt)
    raw = (response.text or "").strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    print("RAW MODEL OUTPUT:", repr(raw))
    try:
        data = json.loads(raw)
        return data.get("actions", []), (data.get("reply") or "").strip()
    except json.JSONDecodeError:
        print("Could not parse the model output as JSON")
        return [], ""