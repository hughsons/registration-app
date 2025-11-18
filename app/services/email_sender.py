# app/services/email_sender.py
import smtplib
from email.message import EmailMessage
from app.config import settings


def send_welcome_email(to_email: str, full_name: str) -> None:
    """
    Sends a simple welcome email via SMTP settings (or local MailHog).
    """
    msg = EmailMessage()
    msg["Subject"] = "Welcome to the Registration App"
    msg["From"] = settings.from_email
    msg["To"] = to_email
    msg.set_content(f"Hi {full_name},\n\nThanks for registering!\n\n— Registration App")

    if settings.smtp_use_tls:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
            s.starttls()
            if settings.smtp_user:
                s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
    else:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
            if settings.smtp_user:
                s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
