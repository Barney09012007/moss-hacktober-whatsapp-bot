import os
import json
from dotenv import load_dotenv
from google import genai
from data import get_open_todos
from prompt import PROMPT

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME")

def interpret_reply(text):
    todos = [t["task"] for t in get_open_todos()]
    prompt = PROMPT.replace("{{TODOS}}", json.dumps(todos)).replace("{{MESSAGE}}", text)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    raw = response.text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw).get("actions", [])
    except json.JSONDecodeError:
        return []