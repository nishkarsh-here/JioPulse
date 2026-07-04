import random
import time
from datetime import datetime, timedelta, timezone

import streamlit as st

from src.database.db import store_reset_token, verify_reset_token, reset_teacher_password
from src.utils.email import send_email, email_is_configured


def _generate_code():
    return f"{random.randint(0, 999999):06d}"


def _close():
    st.session_state.show_reset_password = False
    st.session_state.pop("reset_password_step", None)
    st.session_state.pop("reset_password_email", None)
    st.rerun()


@st.dialog("Reset Password")
def reset_password_dialog():
    step = st.session_state.get("reset_password_step", "request")

    if step == "request":
        st.write("Enter your registered email and we'll send you a reset code.")
        email = st.text_input("Email", placeholder="you@example.com")

        c1, c2 = st.columns(2)
        with c1:
            send_clicked = st.button("Send reset code", type='primary', width='stretch')
        with c2:
            cancel_clicked = st.button("Cancel", width='stretch')

        if cancel_clicked:
            _close()

        if send_clicked:
            if not email:
                st.warning("Please enter your email")
            elif not email_is_configured():
                st.error("Email sending isn't configured on this server yet.")
            else:
                code = _generate_code()
                expires_at = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
                store_reset_token(email, code, expires_at)
                send_email(
                    email,
                    "Your JioPulse password reset code",
                    f"Your JioPulse password reset code is {code}. It expires in 15 minutes.\n\n"
                    "If you didn't request this, you can safely ignore this email."
                )
                st.session_state.reset_password_email = email
                st.session_state.reset_password_step = "verify"
                st.rerun()

    else:
        email = st.session_state.get("reset_password_email", "")
        st.info("If that email is registered, a code has been sent to it.")
        st.write(f"Enter the code sent to **{email}** and choose a new password.")

        code = st.text_input("Reset code", placeholder="123456")
        new_password = st.text_input("New password", type='password')
        confirm_password = st.text_input("Confirm new password", type='password')

        c1, c2 = st.columns(2)
        with c1:
            confirm_clicked = st.button("Reset Password", type='primary', width='stretch')
        with c2:
            cancel_clicked = st.button("Cancel", width='stretch')

        if cancel_clicked:
            _close()

        if confirm_clicked:
            if not code or not new_password:
                st.warning("Please fill all the fields")
            elif new_password != confirm_password:
                st.warning("Passwords don't match")
            elif not verify_reset_token(email, code):
                st.error("Invalid or expired code")
            else:
                reset_teacher_password(email, new_password)
                st.success("Password reset! You can log in now.")
                time.sleep(1)
                _close()
