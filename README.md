# JioPulse

**AI-powered attendance, reimagined for the modern classroom.**

JioPulse takes attendance in seconds. Snap a single photo of the room and computer
vision marks everyone present, run a quick voice roll-call, or let students join a
class with a QR code. On top of that, an in-app assistant answers questions about
your attendance data and explains class policies in plain English.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/App-Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Landing-Flask-000000?logo=flask&logoColor=white">
  <img alt="Gemini" src="https://img.shields.io/badge/AI-Gemini-8E75B2?logo=googlegemini&logoColor=white">
  <img alt="Supabase" src="https://img.shields.io/badge/DB-Supabase-3FCF8E?logo=supabase&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-C8102E">
</p>

---

## Features

- **📸 Face attendance** — recognise every enrolled student from one classroom photo using facial embeddings (dlib).
- **🎙️ Voice attendance** — students say a short phrase; voice biometrics match them against stored signatures.
- **📱 QR enrolment** — every subject gets a unique join code and QR for instant, form-free enrolment.
- **✨ AI assistant** *(new)* — an agentic, retrieval-augmented helper. Ask *"which students are below 75% in CS101?"* and get answers grounded in your live data, or ask *"how does voice attendance work?"* and it retrieves the policy and explains it. Students only ever see their own records.
- **☁️ Cloud backend** — Supabase (PostgreSQL) for auth, rosters and attendance logs.
- **🎨 Clean, responsive UI** — a Streamlit app plus a marketing site built in Flask.

---

## Project structure

This is a monorepo with two deployable parts:

```
JioPulse/
├── app/                  # Streamlit application — the product itself
│   ├── app.py
│   ├── requirements.txt
│   └── src/
│       ├── ai/           # NEW: AI assistant (RAG + agent)
│       │   ├── llm.py            # Gemini client wrapper (OpenAI-compatible endpoint)
│       │   ├── knowledge_base.py # chunk + embed + retrieve (RAG)
│       │   ├── tools.py          # function-calling tools over live data
│       │   ├── agent.py          # the tool-using agent loop
│       │   └── knowledge/        # attendance handbook used for retrieval
│       ├── components/   # dialogs, header, footer, cards
│       ├── database/     # Supabase access layer
│       ├── pipelines/    # face + voice ML pipelines
│       ├── screens/      # home / teacher / student
│       └── ui/           # shared styling
└── landing/              # Flask marketing site (deploys to Vercel)
    ├── app.py
    ├── vercel.json
    ├── templates/index.html
    └── static/
```

---

## How the AI assistant works

The assistant is intentionally small and transparent — "agentic RAG" rather than a black box:

1. **Retrieval (RAG).** Markdown in `app/src/ai/knowledge/` is split into chunks and embedded with Gemini's `text-embedding-004`. At query time the most relevant chunks are pulled back by cosine similarity. The index is built once and cached.
2. **Tools.** The agent is given function-calling tools that read *live* data through the existing database layer — an attendance overview, a per-subject breakdown, a low-attendance finder, a single-student lookup, and a policy search (the RAG step is itself a tool).
3. **Agent loop.** The model decides which tools to call, reads the results, and may chain several calls before composing a grounded answer. It never invents figures, and student access is scoped to the signed-in student.

The assistant runs on **Google Gemini's free tier** via its OpenAI-compatible API, so it costs nothing to run. It degrades gracefully: with no `GEMINI_API_KEY` set, the app runs exactly as before and the assistant simply asks you to add a key (get one free at [aistudio.google.com](https://aistudio.google.com/apikey)).

---

## Tech stack

| Layer | Technology |
|-------|------------|
| App framework | Streamlit |
| Landing site | Flask (served on Vercel) |
| Vision | dlib + `face_recognition_models`, scikit-learn |
| Voice | Resemblyzer, Librosa |
| Database / auth | Supabase (PostgreSQL), bcrypt |
| AI assistant | Gemini (chat + embeddings, free tier), NumPy retrieval |
| QR codes | segno |

---

## Getting started

### Prerequisites
- **Python 3.12+**
- A **Supabase** project (URL + key)
- A free **Gemini API key** (only needed for the assistant)
- A **Gmail App Password** (only needed for teacher password-reset emails)

### Run the app

```bash
git clone https://github.com/<your-username>/JioPulse.git
cd JioPulse/app

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# configure secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with your Supabase + Gemini + Gmail keys

streamlit run app.py
```

### Run the landing site

```bash
cd JioPulse/landing
pip install -r requirements.txt
python app.py          # http://localhost:5002
```

---

## Deployment

- **App → Streamlit Community Cloud.** Point it at `app/app.py` and add `SUPABASE_URL`, `SUPABASE_KEY`, `GEMINI_API_KEY`, `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` under *Secrets*. After deploying, update the public app URL in `landing/templates/index.html` and `app/src/components/dialog_share_subject.py`.
- **Landing → Vercel.** Import the repo, set the **Root Directory** to `landing/` (it ships with `vercel.json`), and deploy.

---

## Configuration

| Key | Where | Purpose |
|-----|-------|---------|
| `SUPABASE_URL` | `app/.streamlit/secrets.toml` | Supabase project URL |
| `SUPABASE_KEY` | `app/.streamlit/secrets.toml` | Supabase API key |
| `GEMINI_API_KEY` | secrets **or** environment | Powers the AI assistant (free tier) |
| `GMAIL_ADDRESS` | secrets **or** environment | Sender address for password-reset emails |
| `GMAIL_APP_PASSWORD` | secrets **or** environment | Gmail App Password (not your login password) |

---

## License

Released under the MIT License — see [LICENSE](LICENSE).
