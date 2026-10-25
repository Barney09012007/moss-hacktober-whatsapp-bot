from ai import interpret_reply

for msg in [
    "finished leetcode",
    "done with LeetCode and add revise OS notes",
    "what's the weather",
]:
    print(msg, "->", interpret_reply(msg))