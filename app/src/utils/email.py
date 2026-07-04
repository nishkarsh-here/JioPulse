"""Minimal email sending for teacher password resets.

Uses Gmail SMTP over SSL via the stdlib smtplib - no extra pip dependency,
no third-party account beyond a Gmail App Password.
"""
import os
import smtplib
from email.mime.text import MIMEText

import streamlit as st

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def _get_secret(name):
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return value or os.environ.get(name)


def email_is_configured():
    return bool(_get_secret("GMAIL_ADDRESS") and _get_secret("GMAIL_APP_PASSWORD"))


def send_email(to_addr, subject, body):
    """Send a plain-text email. Returns True on success, False otherwise."""
    sender = _get_secret("GMAIL_ADDRESS")
    app_password = _get_secret("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_addr

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(sender, app_password)
            server.sendmail(sender, [to_addr], msg.as_string())
        return True
    except Exception:
        return False
