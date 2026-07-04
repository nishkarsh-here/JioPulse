import streamlit as st
from src.database.db import enroll_student_to_subject, get_all_subjects, get_student_subjects
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    student_id = st.session_state.student_data['student_id']

    already_enrolled_ids = {
        node['subjects']['subject_id'] for node in get_student_subjects(student_id)
    }
    available_subjects = [s for s in get_all_subjects() if s['subject_id'] not in already_enrolled_ids]

    tab_browse, tab_code = st.tabs(["Browse Subjects", "I have a code"])

    with tab_browse:
        if not available_subjects:
            st.info("No new subjects available to enroll in right now.")
        else:
            search = st.text_input("Search by name, code, or teacher", placeholder="e.g. Machine Learning")
            filtered = available_subjects
            if search:
                q = search.lower()
                filtered = [
                    s for s in available_subjects
                    if q in s['name'].lower()
                    or q in s['subject_code'].lower()
                    or q in (s.get('teachers') or {}).get('name', '').lower()
                ]

            if not filtered:
                st.info("No subjects match your search.")

            for s in filtered:
                teacher_name = (s.get('teachers') or {}).get('name', 'Unknown teacher')
                c1, c2 = st.columns([3, 1], vertical_alignment='center')
                with c1:
                    st.write(f"**{s['name']}** ({s['subject_code']}) · Section {s['section']} · {teacher_name}")
                with c2:
                    if st.button("Enroll", key=f"browse_enroll_{s['subject_id']}", width='stretch'):
                        enroll_student_to_subject(student_id, s['subject_id'])
                        st.success(f"Enrolled in {s['name']}!")
                        time.sleep(1)
                        st.rerun()

    with tab_code:
        st.write('Enter the subject code provided by your teacher to enroll')
        join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

        if st.button('Enroll now', type='primary', width='stretch'):
            if join_code:
                res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
                if res.data:
                    subject = res.data[0]

                    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                    if check.data:
                        st.warning('You are already enrolled in this program')
                    else:
                        enroll_student_to_subject(student_id, subject['subject_id'])
                        st.success('Succesfully enrolled!')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning('No subject found with that code')
            else:
                st.warning('Please enter a subject code')

    st.divider()
    if st.button("Cancel", width='stretch'):
        st.rerun()
