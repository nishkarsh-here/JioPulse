import streamlit as st
from src.database.db import create_subject, subject_code_exists



@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    c1, c2 = st.columns(2)
    with c1:
        create_clicked = st.button("Create Subject Now", type='primary', width='stretch')
    with c2:
        cancel_clicked = st.button("Cancel", width='stretch')

    if cancel_clicked:
        st.rerun()

    if create_clicked:
        if sub_id and sub_name and sub_section:
            if subject_code_exists(sub_id):
                st.warning("Subject code already exists, please choose another")
            else:
                try:
                    create_subject(sub_id, sub_name, sub_section, teacher_id)
                    st.toast("Subject Created Succesfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the fields")
