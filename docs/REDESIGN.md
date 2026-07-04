# JioPulse — Portfolio Enhancement Plan (AI/ML/DS focus)

> Status: **Active plan.** This replaces the earlier "big SaaS rebuild" draft, which was
> over-scoped once we established the real goal.

## The goal (locked)

This is a **portfolio project** for someone targeting **AI/ML / Data Science roles.** So it is
optimized for how such a project is actually judged:

- A recruiter/engineer spends ~90 seconds on it, then it becomes an **interview talking point.**
- ML/DS reviewers reward: **rigorous evaluation, sound methodology, GenAI/agentic depth, data
  communication, and the ability to explain trade-offs.** They do *not* reward feature breadth or
  SaaS plumbing.
- Polish and UI *help* (they show you finish work and make the demo land) but must not displace the
  ML substance. We get "best UI" in the two places it pays off most: the **landing page** and
  **data visualization**.

### Decisions locked
- **Stay on Streamlit** for the app. It's data-science-native and reads well for ML/DS roles; a
  React rebuild would waste time showcasing the wrong skills.
- **"Best UI" lives in:** (1) a stunning standalone **landing page**, and (2) beautiful, interactive
  **data viz / model-performance dashboards** inside the app (which double as a DS signal), plus
  (3) general polish of the Streamlit app to "clean and modern."
- **Cut entirely:** the Next.js app rebuild, admin/multi-tenant/parent/gamification features,
  SIS/SSO integration. (We *mention* production concerns in the README as a maturity signal, but
  don't build them.)

---

## Where the project is thin (the gaps that matter for ML/DS)

| Gap | Why it matters for these roles |
|---|---|
| **No model evaluation** anywhere | This is *the* line between "used a library" and "does ML." Biggest gap. |
| Agentic RAG not evaluated/documented | GenAI is the hottest hiring area; an eval'd, explained agent is a standout. |
| **No supervised modeling** | The classic DS workflow (features→train→evaluate) is entirely absent. |
| No notebooks / no visible process | Reviewers want to see how you think, not just the final app. |
| README has no demo media, no ML story | Often the only thing a reviewer reads. |
| Registration/biometric wall before any value | Kills the 90-second demo; reviewers won't climb it. |

---

## The plan (priority order)

### 1. Rigorous evaluation of the face + voice pipelines  ⟵ highest ML signal
- Build a labeled **test set** (real photos/clips or a documented synthetic/augmented set).
- Report **accuracy, precision, recall, F1** for the face matcher and the voice matcher.
- **Threshold analysis**: the pipelines match on distance thresholds — show the precision/recall
  trade-off and justify the chosen cutoff (ROC / PR curves).
- **Failure analysis**: characterize where it breaks (small/distant faces, lighting, angle,
  look-alikes; short/noisy audio). Honest limitations = maturity signal.
- Deliver as a **notebook** (`notebooks/01_face_voice_eval.ipynb`) + a summary + plots surfaced in
  the app and README.

### 2. Deepen and evaluate the agentic RAG assistant  ⟵ the GenAI centerpiece
- Document the RAG pipeline (chunking, embeddings via Gemini `text-embedding-004`, retrieval) and
  **evaluate retrieval quality** (are the right chunks returned for a question set?).
- Build a small **agent eval set** (question → expected answer/behavior) that runs and reports
  correctness. LLM evals are rare in portfolios and a strong differentiator.
- Add guardrails notes (PII-to-LLM awareness, prompt-injection surface, rate-limit handling) — talks
  well in interviews.
- Notebook (`notebooks/02_rag_agent_eval.ipynb`) + README section.

### 3. At-risk student prediction model  ⟵ the supervised-DS story + best-UI dashboard
- Frame it: from attendance history, predict P(student drops below the min-attendance policy).
- Do it *properly*: feature engineering, train/test split, model comparison (e.g., logistic
  regression vs. gradient boosting), metrics, calibration, feature importance. Synthetic data is
  fine if documented.
- Surface predictions in the app as a **beautiful, interactive dashboard** (Plotly/Altair) — this is
  where "best UI" and "DS skill" become the same deliverable.
- Notebook (`notebooks/03_at_risk_model.ipynb`) + model card + in-app dashboard.

### 4. Stunning landing page  ⟵ the "best UI" flex, first impression
- A bounded, high-visibility, animated landing page (motion, animated flow diagrams, clear story).
- Deployed on Vercel (free); links into the Streamlit app.
- Tells the story: problem → multi-modal attendance → agentic AI → *and how it was evaluated*.
- (Tooling: prefer whatever gives the best result with the least build friction — a polished static
  site with a modern animation lib, or a small Next build if the toolchain is available.)

### 5. Polish the Streamlit app to "clean and modern"
- Extend the existing design system (`app/src/ui/base_layout.py`, dark/light theme).
- Consistent components, spacing, type; `streamlit-lottie` micro-animations; good empty states and
  skeletons; the interactive data-viz from #3.
- One-click **"Try as demo teacher / demo student"** login + **seed data** so a reviewer sees value
  in 15 seconds with zero typing.

### 6. Documentation & presentation
- **README rebuilt** around an evaluation-forward narrative, with a **demo GIF/video** at the top,
  architecture diagram, and "interesting engineering" highlights.
- **Model cards** for each model (purpose, data, metrics, limitations).
- A short **write-up/blog** ("building *and evaluating* multi-modal attendance + an agentic RAG
  assistant") — communication is a rare, rewarded signal.
- One or two README sentences noting production concerns we deliberately didn't build (SIS/SSO,
  biometric consent for minors, liveness) — signals maturity without the work.

---

## Suggested build order this cycle

Two valid entry points; we start with the **visible UI win** per your priority, then substance:

1. **Landing page** (#4) — immediate visible payoff.
2. **Evaluation notebook** (#1) — highest ML signal.
3. **At-risk model + dashboard** (#3) — DS story + best-UI data viz.
4. **RAG/agent eval** (#2).
5. **Streamlit polish + demo logins** (#5).
6. **README + model cards + write-up** (#6).

Each item is independent and leaves the app working. Nothing here requires a rewrite or breaks the
live Streamlit app.
