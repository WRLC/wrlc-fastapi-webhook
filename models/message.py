"""
Email model
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Message(BaseModel):
    """
    Email object
    """
    subject: str = Field(title="Subject", examples=["Email subject"])
    body: str = Field(title="Body", examples=["Hi, this is an email body"])
    to: str = Field(title="To", examples=["recipient1@domain.com,recipient2@domain.com"])
    sender: str = Field(title="Sender", examples=["sender@domain.com"])

    def construct_email(self) -> MIMEMultipart:
        """
        Construct the email object

        :return: dict
        """
        to = ''
        if isinstance(self.to, str):
            to = self.to
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = to
        msg.attach(MIMEText(self.body, 'html'))

        return msg

    def send_email(self, msg) -> None:
        """
        Send the email
        """
        smtp = os.getenv('SMTP_SERVER') or ''
        ssl = os.getenv('SMTP_SSL') or "False"
        to = self.to.split()  # pylint: disable=E1101

        if ssl == "True":
            ssl_server = smtplib.SMTP_SSL(smtp)
            ssl_server.sendmail(self.sender, to, msg.as_string())
            ssl_server.quit()
        else:
            server = smtplib.SMTP(smtp)
            server.sendmail(self.sender, to, msg.as_string())
            server.quit()
