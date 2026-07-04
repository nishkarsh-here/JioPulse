from src.database.config import supabase
import bcrypt



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 



def create_teacher(username, password, name, email):

    data = { "username" : username, "password": hash_pass(password), "name": name, "email": email}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def store_reset_token(email, token, expires_at):
    response = supabase.table("teachers").update(
        {"reset_token": token, "reset_token_expires": expires_at}
    ).eq("email", email).execute()
    return len(response.data) > 0


def verify_reset_token(email, token):
    response = supabase.table("teachers").select("teacher_id, reset_token, reset_token_expires").eq("email", email).execute()
    if not response.data:
        return False

    teacher = response.data[0]
    if not teacher.get("reset_token") or teacher["reset_token"] != token:
        return False

    expires_at = teacher.get("reset_token_expires")
    if not expires_at:
        return False

    from datetime import datetime, timezone
    if datetime.fromisoformat(expires_at) < datetime.now(timezone.utc):
        return False

    return True


def reset_teacher_password(email, new_password):
    response = supabase.table("teachers").update(
        {"password": hash_pass(new_password), "reset_token": None, "reset_token_expires": None}
    ).eq("email", email).execute()
    return len(response.data) > 0


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def subject_code_exists(subject_code):
    response = supabase.table("subjects").select("subject_id").eq("subject_code", subject_code).execute()
    return len(response.data) > 0


def get_all_subjects():
    response = supabase.table('subjects').select("subject_id, subject_code, name, section, teachers(name)").execute()
    return response.data


def get_subject_roster(subject_id):
    response = supabase.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data

