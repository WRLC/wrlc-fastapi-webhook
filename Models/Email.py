"""
Email model
"""
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Email(BaseModel):
    """
    Email object
    """
    subject: str
    body: str
    to: str
    sender: str
    smtp: str = os.getenv('SMTP_SERVER')
    port: int = os.getenv('SMTP_PORT')
    ssl: bool = os.getenv('SMTP_SSL')

    def construct_email(self) -> MIMEMultipart:
        """
        Construct the email object

        :return: dict
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.to
        msg.attach(MIMEText(self.body, 'html'))

        return msg
