import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def send_email(to_email, subject, body):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = os.getenv("EMAIL_SMTP")
    smtp_password = os.getenv("PASSWORD_FOR_EMAIL")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_email, msg.as_string())
    except Exception as e:
        print(f'Failed to send email: {e}')