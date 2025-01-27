from crewai.tools import BaseTool
import imaplib
import os

class MoveToSpamTool(BaseTool):
    name: str = "MoveToSpamTool"
    description: str = "Move mail with id emailid to spam if was classified as a SPAM"
    
    def _run(self, query: str, email_id: int) -> str:
        """
        Move mail with id emailid to spam if was classified as a SPAM
        """
        username = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        message = email_ids[email_id]
        mail.copy(message, '[Gmail]/Spam')
        mail.store(message, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.logout()
        return("Moved to spam!")
    