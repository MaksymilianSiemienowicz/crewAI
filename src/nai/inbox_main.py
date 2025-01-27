from inbox_managing_crew import InboxManaginCrew
import imaplib
import email
from email.message import EmailMessage
import time
import ssl
import smtplib
from email.header import decode_header
import subprocess
import os
import csv

username = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

what_model_is_used = "gemini"
what_metrics_are_gathered_for = "spam"
spam = 0
order = 0
other = 0
another = 0
deal = 0


csv_data = [[],[]]
csv_data[0] = ["catgory", "model", "spam", "other", "deals", "another", "order"]

def run(content, sender, subject, mail_id):
    inputs = {
        'content': content,
        'sender': sender,
        'subject': subject,
        'mail_id' : mail_id
    }
    ai = InboxManaginCrew().crew()
    crew_output = ai.kickoff(inputs=inputs)
    return crew_output.raw
    

def isNewMessage(mail):

    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("Błąd podczas pobierania wiadomości.")
        return False

    new = messages[0].split()

    return len(new) > 0

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

            mail.select("inbox")

            if isNewMessage(mail):
                
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
                            global spam, other, deal, order, another
                            global csv_data
                            global what_model_is_used
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print(f"Treść wiadomości:\n{body}")
                                        x = run(body,from_,subject,email_id)
                                print("X = ",x)
                                if x.strip().lower().startswith("moved to spam"):

                                    spam += 1
                                elif x.strip().lower().startswith("moved to other"):
                                    other += 1
                                elif x.strip().lower().startswith("moved to deals"):

                                    deal += 1
                                elif x.strip().lower().startswith("moved to orders"):

                                    order += 1
                                else:
                                    another += 1
                                print("------------------------------------------------")
                                print(f"Spam: {spam}")
                                print(f"Inne: {another}")
                                print(f"Other: {other}")
                                print(f"Order: {order}")
                                print("------------------------------------------------")
                                csv_data[1] = [what_metrics_are_gathered_for, what_model_is_used, spam, other, order, deal, another]
                                with open(what_metrics_are_gathered_for+"_"+what_model_is_used+"_metrics.csv", "w") as file:
                                    writer = csv.writer(file)
                                    writer.writerows(csv_data)
                                break
                            else:
                                body = msg.get_payload(decode=True).decode()
                                print(f"Treść wiadomości:\n{body}")
                                x = run(body,from_,subject,email_id)
                                print("X = ",x)
                                if x.strip().lower().startswith("moved to spam"):

                                    spam += 1
                                elif x.strip().lower().startswith("moved to other"):
                                    other += 1
                                elif x.strip().lower().startswith("moved to deals"):

                                    deal += 1
                                elif x.strip().lower().startswith("moved to orders"):

                                    order += 1
                                else:
                                    another += 1
                            print("------------------------------------------------")
                            print(f"Spam: {spam}")
                            print(f"Inne: {another}")
                            print(f"Other: {other}")
                            print(f"Order: {order}")
                            print("------------------------------------------------")
                            csv_data[1] = [what_metrics_are_gathered_for, what_model_is_used, spam, other, order, deal, another]
                            with open(what_metrics_are_gathered_for+"_"+what_model_is_used+"_metrics.csv", "w") as file:
                                writer = csv.writer(file)
                                writer.writerows(csv_data)
            time.sleep(delay)

    except KeyboardInterrupt:
        print("Monitorowanie przerwane.")




def start():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")


        mail.login(username, password)
        mail.select("inbox")

        monitor_new_emails(mail, delay=10)
        mail.logout()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")