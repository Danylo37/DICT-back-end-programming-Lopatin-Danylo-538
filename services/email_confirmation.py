"""Email service — sends confirmation emails via SMTP."""

import os
import smtplib
from email.mime.text import MIMEText


def send_confirmation_email(receiver: str, token: str) -> None:
    """
    Send an email confirmation link to the newly registered user.
    Uses Gmail SMTP with credentials from .env.
    """
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    base_url = os.getenv("BASE_URL")

    confirm_url = f"{base_url}/confirm/{token}"

    msg = MIMEText(
        f"Hello!\n\n"
        f"Please confirm your email address by clicking the link below:\n\n"
        f"{confirm_url}\n\n"
        f"If you did not register, simply ignore this email."
    )
    msg["Subject"] = "Confirm your Guestbook registration"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
