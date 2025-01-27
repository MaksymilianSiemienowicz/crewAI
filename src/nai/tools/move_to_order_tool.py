from crewai.tools import BaseTool
import imaplib
import os

class MoveToOrdersTool(BaseTool):
    name: str = "MoveToOrdersTool"
    description: str = "Move mail with id emailid to orders if was classified as an ORDER"
    
    def _run(self, query: str, email_id: int) -> str:
        """
        Move mail with id emailid to orders if was slassified as a ORDER
        """
        username = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        message = email_ids[email_id]
        mail.copy(message, 'orders')
        mail.store(message, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.logout()
        return("Moved to orders!")