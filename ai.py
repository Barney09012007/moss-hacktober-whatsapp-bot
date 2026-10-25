import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from data import get_open_todos
from prompt import PROMPT

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL_NAME")

FENCE = "`" * 3  # three backticks, built this way so it can't get mangled when pasted

# Fast config: JSON output, deterministic, and minimal "thinking". Gemini 3.x models think by
# default (3.5 Flash defaults to MEDIUM), which adds seconds to a simple classification task.
try:
    _FAST = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0,
        thinking_config=types.ThinkingConfig(thinking_level="minimal"),
    )
except Exception:  # older google-genai SDK without thinking_level
    _FAST = None
_PLAIN = types.GenerateContentConfig(response_mime_type="application/json", temperature=0)
_use_fast = _FAST is not None


def _generate(prompt):
    """Try the fast config; if the model/SDK rejects it, fall back to a plain call (once)."""
    global _use_fast
    if _use_fast:
        try:
            return client.models.generate_content(model=MODEL, contents=prompt, config=_FAST)
        except Exception as e:
            if any(k in str(e) for k in ("INVALID_ARGUMENT", "thinking", "400")):
                print("Fast config not accepted by this model, using plain config:", e)
                _use_fast = False
            else:
                raise
    return client.models.generate_content(model=MODEL, contents=prompt, config=_PLAIN)


def _strip_fences(raw):
    raw = raw.strip()
    raw = raw.removeprefix(FENCE + "json").removeprefix(FENCE).removesuffix(FENCE)
    return raw.strip()


def interpret_reply(text):
    todos = [t["task"] for t in get_open_todos()]
    now = datetime.now().strftime("%A, %Y-%m-%d %H:%M")
    prompt = (PROMPT.replace("{{NOW}}", now)
                    .replace("{{TODOS}}", json.dumps(todos))
                    .replace("{{MESSAGE}}", text))
    t0 = time.perf_counter()
    response = _generate(prompt)
    print(f"[timing] AI call took {time.perf_counter() - t0:.1f}s")
    raw = _strip_fences(response.text or "")
    print("RAW MODEL OUTPUT:", repr(raw))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Could not parse the model output as JSON")
        return [], ""
    if not isinstance(data, dict):
        return [], ""
    actions = data.get("actions") or []
    reply = (data.get("reply") or "").strip()
    return [a for a in actions if isinstance(a, dict)], reply