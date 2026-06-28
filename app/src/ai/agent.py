"""The JioPulse agent.

A compact tool-using loop: the model can call data and policy tools, read the
results, and decide whether to call more tools or answer. This gives us
"agentic RAG" - retrieval is just one of the tools the agent reaches for.
"""
import json

from src.ai.llm import chat
from src.ai.tools import get_tools

MAX_STEPS = 5


def _system_prompt(ctx):
    role = ctx.get("role", "user")
    name = ctx.get("name", "there")
    audience = (
        "a teacher managing subjects and classroom attendance"
        if role == "teacher"
        else "a student tracking their own attendance"
    )
    return (
        f"You are JioPulse AI, the built-in assistant of the JioPulse attendance "
        f"platform. You are helping {name}, who is {audience}.\n\n"
        "Guidelines:\n"
        "- Use the provided tools to fetch real attendance data before answering "
        "questions about numbers, students, or subjects. Never invent figures.\n"
        "- For questions about rules, policies, privacy, or how a feature works, "
        "call search_policy_knowledge and ground your answer in what it returns.\n"
        "- A student may only see their own data; never expose other students' "
        "records to a student.\n"
        "- Be concise and practical. Use short paragraphs or tight bullet lists. "
        "Report percentages as whole or one-decimal numbers.\n"
        "- If a tool returns no data, say so plainly instead of guessing.\n"
        "- Stay within attendance, subjects, students and JioPulse features."
    )


def run_agent(user_message, history, ctx):
    """Run one assistant turn.

    history: list of {"role": "user"|"assistant", "content": str} prior turns.
    Returns {"answer": str, "trace": [{"tool", "args"}...]}.
    """
    tools_schema, dispatch = get_tools(ctx.get("role"))

    messages = [{"role": "system", "content": _system_prompt(ctx)}]
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    trace = []
    for _ in range(MAX_STEPS):
        resp = chat(messages, tools=tools_schema)
        msg = resp.choices[0].message

        if not msg.tool_calls:
            return {"answer": msg.content or "", "trace": trace}

        # record the assistant's tool-call request
        messages.append({
            "role": "assistant",
            "content": msg.content or None,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })

        # run each requested tool and feed results back
        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            trace.append({"tool": name, "args": args})
            fn = dispatch.get(name)
            try:
                result = fn(args, ctx) if fn else {"error": f"Unknown tool {name}"}
            except Exception as exc:  # never let a tool crash the chat
                result = {"error": f"{type(exc).__name__}: {exc}"}
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": name,
                "content": json.dumps(result, default=str),
            })

    # ran out of tool steps - ask for a final answer without tools
    resp = chat(messages)
    return {"answer": resp.choices[0].message.content or "", "trace": trace}
