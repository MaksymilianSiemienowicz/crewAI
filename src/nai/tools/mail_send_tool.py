from crewai.tools import BaseTool
from email.message import EmailMessage
import ssl
import smtplib
from email.header import decode_header
import os

class SendMail(BaseTool):
    name: str = "SendMail"
    description: str = "Send Email"
    
    def _run(self, query: str, recipient_email_address: str, content: str, subject: str) -> str:
        """
        Seand email with provided: sender, content, subject
        """
        username = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        email = EmailMessage()
        email['From'] = username
        email['To'] = recipient_email_address
        email['Subject'] = subject
        email.set_content(content)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(username, password)
            smtp.sendmail(username, recipient_email_address, email.as_string())
        return("Mail sent!")