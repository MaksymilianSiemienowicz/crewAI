from deals_managing_crew import DealsManaginCrew
import imaplib
import email
from email.message import EmailMessage
import time
import ssl
import smtplib
from email.header import decode_header
import os

username = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

def run(content, sender, subject, mail_id):
    inputs = {
        'content': content,
        'sender': sender,
        'subject': subject,
        'mail_id' : mail_id
    }
    ai = DealsManaginCrew().crew()
    ai.kickoff(inputs=inputs)

def isNewMessage(mail, old):

    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("Błąd podczas pobierania wiadomości.")
        return False

    new = messages[0].split()

    return len(new) > len(old)

def monitor_new_emails(mail, delay=30):
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("Błąd podczas inicjalizacji wiadomości.")
        return
    
    email_ids = messages[0].split()
    print(f"Początkowa liczba wiadomości: {len(email_ids)}")

    try:
        # Główna petla monitorujaca
        while True:

            mail.select("deals")

            if isNewMessage(mail,email_ids):
                
                print("Nowa wiadomość!")
                status, messages = mail.search(None, "ALL")

                if status == "OK":

                    email_ids = messages[0].split()

                    last_mail = email_ids[len(email_ids)-1]
                    email_id = len(email_ids)-1
                    status, msg_data = mail.fetch(last_mail, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")

                            from_ = msg.get("From")
                            print(f"Temat: {subject}")
                            print(f"Nadawca: {from_}")

                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print(f"Treść wiadomości:\n{body}")
                                        run(body,from_,subject,email_id)
                                        break
                            else:
                                body = msg.get_payload(decode=True).decode()
                                print(f"Treść wiadomości:\n{body}")
                                run(body,from_,subject,email_id)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("Monitorowanie przerwane.")

    
def start():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")


        mail.login(username, password)
        mail.select("deals")

        monitor_new_emails(mail, delay=10)
        mail.logout()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")