import pandas as pd
import ssl
import smtplib
from email.header import decode_header
import os
from email.message import EmailMessage
df = pd.read_csv('./spam_mail.csv')
import time
def _run(recipient_email_address: str, content: str, subject: str) -> str:
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

for i in range(100):
    _run("naiprojekt31@gmail.com", df.content[i], df.subject[i])
    print("Mail sent! - "+str(i))
    time.sleep(3)