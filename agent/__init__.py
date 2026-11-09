"""Wrapper that runs the core agent and prints thoughts, the todo list and the decision."""

from .agent import build_agent

class ClaimsAgent:
    def __init__(self):
        self.agent = build_agent()

    def process_claim(self, claim_data: dict, log_thoughts=False, log_tool_calls=False):
        details = "\n".join(f"{k} - {v or '(none)'}" for k, v in claim_data.items())
        prompt = f"Review this expense claim.\n---\n{details}\n---"
        inputs = {"messages": [{"role": "user", "content": prompt}]}

        final = None
        for mode, chunk in self.agent.stream(inputs, stream_mode=["updates", "values"]):
            if mode == "values":
                final = chunk
                continue
            for update in chunk.values():
                msgs = update.get("messages") if isinstance(update, dict) else None
                if not msgs:
                    continue
                for m in msgs if isinstance(msgs, list) else [msgs]:
                    # Only AI messages that are followed by tool calls; the last
                    # message (no tool calls) is the decision, printed at the end.
                    if m.type != "ai" or not m.tool_calls:
                        continue
                    if log_thoughts:
                        for text in get_text_blocks(m.content):
                            print(f"\nThought: {text.strip()}")
                    if log_tool_calls:
                        for call in m.tool_calls:
                            if call["name"] == "write_todos":
                                print("\nTodo:")
                                for t in call["args"].get("todos", []):
                                    print(f"  {MARK.get(t.get('status'), '[ ]')} {t.get('content')}")

        self._print_decision(claim_data["claim_id"], final)
        return final

    def _print_decision(self, claim_id: str, final) -> None:
        print("\n" + "-" * 40)
        report = (final.get("files") or {}).get(f"/reports/{claim_id}.md")
        if report:
            c = report["content"]
            text = "\n".join(c) if isinstance(c, list) else c
            for line in text.splitlines()[:2]:
                if line.startswith(("DECISION", "APPROVED_AMOUNT")):
                    print(line.replace("_", " ").capitalize())
        print(get_text(final["messages"][-1].content))


MARK = {"pending": "[ ]", "in_progress": "[>]", "completed": "[x]"}

# gemini can return either strings or dict
def get_text_blocks(content):
    if isinstance(content, str):
        if content.strip():
            yield content
        return
    for b in content or []:
        if isinstance(b, dict) and b.get("type") in ("thinking", "text"):
            text = b.get("thinking") or b.get("text") or ""
            if text.strip():
                yield text
                
def get_text(content):
    return "\n".join(get_text_blocks(content))

claims_agent = ClaimsAgent()