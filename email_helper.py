# email_helper.py
import smtplib
from email.message import EmailMessage
from config import email_data
import os
import getpass
import socket


def send_email(subject, body):
    current_dir = os.getcwd()
    folder_name = os.path.basename(current_dir)
    computer_name = socket.gethostname()
    user_name = getpass.getuser()
    new_line = "\n"
    body_with_new_line = (
        f"{body}{new_line}{folder_name} on {computer_name} ({user_name})"
    )
    msg = EmailMessage()
    msg.set_content(body_with_new_line)
    msg["Subject"] = f"{subject} : {folder_name}"
    msg["From"] = email_data["sender_email"]
    msg["To"] = ", ".join(email_data["recipient_emails"])

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_data["sender_email"], email_data["sender_password"])
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
