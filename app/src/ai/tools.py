"""Function-calling tools the agent can invoke.

Each tool reads live data through the existing database layer and returns
plain, JSON-serialisable Python so the model can reason over it. Tools are
scoped by role: a student can only ever see their own record.
"""
import pandas as pd

from src.database import db
from src.ai.knowledge_base import retrieve


# ----------------------------- helpers ------------------------------------
def _student_name_map():
    try:
        return {s["student_id"]: s["name"] for s in db.get_all_students()}
    except Exception:
        return {}


def _teacher_frame(teacher_id):
    """Flat attendance table for everything this teacher owns."""
    logs = db.get_attendance_for_teacher(teacher_id) or []
    names = _student_name_map()
    rows = []
    for r in logs:
        subj = r.get("subjects") or {}
        rows.append({
            "student_id": r.get("student_id"),
            "student": names.get(r.get("student_id"), f"Student {r.get('student_id')}"),
            "subject": subj.get("name"),
            "subject_code": subj.get("subject_code"),
            "present": bool(r.get("is_present")),
        })
    return pd.DataFrame(rows)


# ----------------------------- teacher tools ------------------------------
def get_teacher_overview(args, ctx):
    subjects = db.get_teacher_subjects(ctx["teacher_id"]) or []
    df = _teacher_frame(ctx["teacher_id"])
    overall = round(100 * df["present"].mean(), 1) if not df.empty else None
    return {
        "teacher": ctx.get("name"),
        "subject_count": len(subjects),
        "subjects": [
            {
                "name": s.get("name"),
                "code": s.get("subject_code"),
                "section": s.get("section"),
                "students": s.get("total_students"),
                "classes_held": s.get("total_classes"),
            }
            for s in subjects
        ],
        "overall_attendance_percent": overall,
    }


def get_subject_attendance(args, ctx):
    code = (args or {}).get("subject_code")
    df = _teacher_frame(ctx["teacher_id"])
    if df.empty:
        return {"message": "No attendance has been recorded yet."}
    if code:
        df = df[df["subject_code"].str.lower() == str(code).lower()]
        if df.empty:
            return {"message": f"No records found for subject code {code}."}
    out = []
    for (name, scode), g in df.groupby(["subject", "subject_code"]):
        out.append({
            "subject": name,
            "subject_code": scode,
            "sessions_logged": int(len(g)),
            "present": int(g["present"].sum()),
            "attendance_percent": round(100 * g["present"].mean(), 1),
        })
    return {"subjects": out}


def find_low_attendance_students(args, ctx):
    args = args or {}
    threshold = float(args.get("threshold", 75))
    code = args.get("subject_code")
    df = _teacher_frame(ctx["teacher_id"])
    if df.empty:
        return {"message": "No attendance has been recorded yet."}
    if code:
        df = df[df["subject_code"].str.lower() == str(code).lower()]
    grp = (
        df.groupby(["student", "subject", "subject_code"])["present"]
        .agg(["mean", "count"])
        .reset_index()
    )
    grp["attendance_percent"] = (100 * grp["mean"]).round(1)
    low = grp[grp["attendance_percent"] < threshold].sort_values("attendance_percent")
    return {
        "threshold": threshold,
        "count": int(len(low)),
        "students": [
            {
                "student": r["student"],
                "subject": r["subject"],
                "subject_code": r["subject_code"],
                "attendance_percent": float(r["attendance_percent"]),
                "sessions": int(r["count"]),
            }
            for _, r in low.iterrows()
        ],
    }


def get_student_attendance_record(args, ctx):
    name = (args or {}).get("student_name", "").strip()
    if not name:
        return {"error": "student_name is required."}
    df = _teacher_frame(ctx["teacher_id"])
    if df.empty:
        return {"message": "No attendance has been recorded yet."}
    match = df[df["student"].str.lower().str.contains(name.lower())]
    if match.empty:
        return {"message": f"No student matching '{name}' was found in your records."}
    out = []
    for (sname, scode), g in match.groupby(["subject", "subject_code"]):
        out.append({
            "subject": sname,
            "subject_code": scode,
            "attendance_percent": round(100 * g["present"].mean(), 1),
            "sessions": int(len(g)),
        })
    return {"student": match.iloc[0]["student"], "record": out}


# ----------------------------- student tools ------------------------------
def get_my_attendance(args, ctx):
    logs = db.get_student_attendance(ctx["student_id"]) or []
    if not logs:
        return {"message": "You have no attendance records yet."}
    rows = []
    for r in logs:
        subj = r.get("subjects") or {}
        rows.append({
            "subject": subj.get("name"),
            "subject_code": subj.get("subject_code"),
            "present": bool(r.get("is_present")),
        })
    df = pd.DataFrame(rows)
    out = []
    for (name, scode), g in df.groupby(["subject", "subject_code"]):
        out.append({
            "subject": name,
            "subject_code": scode,
            "attendance_percent": round(100 * g["present"].mean(), 1),
            "attended": int(g["present"].sum()),
            "total": int(len(g)),
        })
    overall = round(100 * df["present"].mean(), 1)
    return {"overall_attendance_percent": overall, "subjects": out}


def get_my_subjects(args, ctx):
    subs = db.get_student_subjects(ctx["student_id"]) or []
    return {
        "subjects": [
            {
                "name": (s.get("subjects") or {}).get("name"),
                "code": (s.get("subjects") or {}).get("subject_code"),
                "section": (s.get("subjects") or {}).get("section"),
            }
            for s in subs
        ]
    }


# ----------------------------- shared (RAG) tool --------------------------
def search_policy_knowledge(args, ctx):
    query = (args or {}).get("query", "")
    hits = retrieve(query, k=4)
    if not hits:
        return {"message": "No policy information is available for that query."}
    return {"passages": [text for text, _score in hits]}


# ----------------------------- registry -----------------------------------
_POLICY_TOOL = {
    "type": "function",
    "function": {
        "name": "search_policy_knowledge",
        "description": "Look up JioPulse attendance rules, policies, privacy, "
                       "and how face/voice/QR features work.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "What to look up."}},
            "required": ["query"],
        },
    },
}

_TEACHER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_teacher_overview",
            "description": "Summary of the teacher's subjects, class counts, "
                           "student counts and overall attendance.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_subject_attendance",
            "description": "Attendance percentage and sessions per subject. "
                           "Optionally filter to one subject code.",
            "parameters": {
                "type": "object",
                "properties": {"subject_code": {"type": "string"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_low_attendance_students",
            "description": "List students below an attendance threshold "
                           "(default 75%), optionally within one subject.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number", "description": "Percent, default 75."},
                    "subject_code": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_attendance_record",
            "description": "Attendance record for one named student across the "
                           "teacher's subjects.",
            "parameters": {
                "type": "object",
                "properties": {"student_name": {"type": "string"}},
                "required": ["student_name"],
            },
        },
    },
    _POLICY_TOOL,
]

_STUDENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_my_attendance",
            "description": "The signed-in student's attendance percentage per "
                           "subject and overall.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_my_subjects",
            "description": "Subjects the signed-in student is enrolled in.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    _POLICY_TOOL,
]

_DISPATCH = {
    "get_teacher_overview": get_teacher_overview,
    "get_subject_attendance": get_subject_attendance,
    "find_low_attendance_students": find_low_attendance_students,
    "get_student_attendance_record": get_student_attendance_record,
    "get_my_attendance": get_my_attendance,
    "get_my_subjects": get_my_subjects,
    "search_policy_knowledge": search_policy_knowledge,
}


def get_tools(role):
    """Return (schema_list, dispatch_map) appropriate for the role."""
    schema = _TEACHER_TOOLS if role == "teacher" else _STUDENT_TOOLS
    return schema, _DISPATCH
