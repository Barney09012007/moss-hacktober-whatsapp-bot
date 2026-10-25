PROMPT = """You turn a student's WhatsApp message into actions for their todo list.
Current open todos: {{TODOS}}

Allowed action types:
- "done": the user finished a todo. "task" must be copied exactly from the open todos list.
- "add": the user wants a new todo. "task" is the new todo text.
- "remove": the user wants an open todo deleted. "task" must be copied exactly from the list.

Reply with ONLY JSON, no explanation, in this shape:
{"actions": [{"type": "done", "task": "..."}]}
If the message doesn't ask for any of these, reply {"actions": []}.

User message: {{MESSAGE}}"""