import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

# Environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using SMTP (e.g., Gmail).
    If credentials are missing, logs the email to console (Mock Mode).
    """
    if not EMAIL_USER or not EMAIL_PASSWORD:
        logger.warning("⚠️ Email credentials missing. Running in MOCK MODE.")
        logger.info(f"📧 [MOCK EMAIL] To: {to_email} | Subject: {subject} | Body: {body}")
        return {"status": "mock_sent", "message": "Mock email logged to console"}

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()

        logger.info(f"✅ Email sent to {to_email}")
        return {"status": "sent", "message": "Email sent successfully"}

    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        return {"status": "error", "error": str(e)}
