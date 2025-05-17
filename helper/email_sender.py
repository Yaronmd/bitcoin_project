import smtplib
import os
from email.message import EmailMessage
from helper.logger_helper import logger

class EmailSender:
    def __init__(self, sender_email, app_password, receiver_email):
        self.sender_email = sender_email
        self.app_password = app_password
        self.receiver_email = receiver_email

    def send_email_with_attachment(self, subject, body, file_path):
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(msg)

            logger.info(f"Email sent to {self.receiver_email} with attachment: {file_name}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

