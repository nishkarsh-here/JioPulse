import streamlit as st

from src.ai.llm import ai_is_configured
from src.ai.agent import run_agent

SUGGESTIONS = {
    "teacher": [
        "Which students are below 75% attendance?",
        "Give me an overview of my subjects",
        "How does voice attendance work?",
    ],
    "student": [
        "What is my attendance percentage?",
        "Which subjects am I enrolled in?",
        "What is the minimum attendance rule?",
    ],
}


def _build_context(role):
    if role == "teacher":
        t = st.session_state.get("teacher_data", {})
        return {"role": "teacher", "name": t.get("name"), "teacher_id": t.get("teacher_id")}
    s = st.session_state.get("student_data", {})
    return {"role": "student", "name": s.get("name"), "student_id": s.get("student_id")}


def _close():
    st.session_state.ai_assistant_open = False
    st.rerun()


@st.dialog("JioPulse AI Assistant", width="large")
def ai_assistant_dialog(role):
    ctx = _build_context(role)
    hist_key = f"ai_chat_{role}"
    history = st.session_state.setdefault(hist_key, [])

    st.caption("Ask about attendance, students, subjects, or how JioPulse works.")

    if not ai_is_configured():
        st.warning(
            "The AI assistant needs an OpenAI key. Add **OPENAI_API_KEY** to "
            "`.streamlit/secrets.toml` (or your environment) to turn it on."
        )
        if st.button("Close", width="stretch"):
            _close()
        return

    # 1) process a question queued on the previous run (keeps transcript ordered)
    pending = st.session_state.pop(f"ai_pending_{role}", None)
    if pending:
        history.append({"role": "user", "content": pending})
        with st.spinner("JioPulse AI is thinking..."):
            try:
                result = run_agent(pending, history[:-1][-8:], ctx)
                answer = result.get("answer") or "I couldn't find an answer to that."
                trace = result.get("trace")
            except Exception as exc:
                answer = f"I couldn't reach the AI service just now ({exc})."
                trace = None
        history.append({"role": "assistant", "content": answer, "trace": trace})

    # 2) transcript
    if not history:
        st.info("Try one of these to get started:")
        for s in SUGGESTIONS.get(role, []):
            st.markdown(f"- {s}")
    for m in history:
        avatar = "✨" if m["role"] == "assistant" else ("👩‍🏫" if role == "teacher" else "🎓")
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])
            if m.get("trace"):
                with st.expander("How I worked this out"):
                    for step in m["trace"]:
                        args = step.get("args") or {}
                        st.caption(f"🔧 `{step['tool']}` {args if args else ''}")

    # 3) input
    with st.form(key=f"ai_form_{role}", clear_on_submit=True):
        user_msg = st.text_input(
            "Your question",
            placeholder="e.g. Which students are below 75% in CS101?",
            label_visibility="collapsed",
        )
        b1, b2 = st.columns([4, 1])
        with b1:
            sent = st.form_submit_button("Ask JioPulse AI", type="primary", width="stretch")
        with b2:
            closed = st.form_submit_button("Close", width="stretch")

    if closed:
        _close()
    if sent and user_msg.strip():
        st.session_state[f"ai_pending_{role}"] = user_msg.strip()
        st.rerun()
