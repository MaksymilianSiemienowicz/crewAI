from crewai.tools import BaseTool
import imaplib
import os

class MoveToDealsTool(BaseTool):
    name: str = "MoveToDealsTool"
    description: str = "Move mail with id emailid to deals if was classified as a DEAL"
    
    def _run(self, query: str, email_id: int) -> str:
        """
        Move mail with id emailid to deal if was slassified as a DEAL
        """
        username = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        message = email_ids[email_id]
        mail.copy(message, 'deals')
        mail.store(message, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.logout()
        return("Moved to deals!")