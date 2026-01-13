from smtplib import SMTP_SSL
from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings
from app.domain.interfaces import InterfaceMessageSender


class SMTPMessageSender(InterfaceMessageSender):
    def create_message(self, send_to: EmailStr, text: str) -> EmailMessage:
        email_message = EmailMessage()

        email_message["Subject"] = 'Извлеченный текст'
        email_message["From"] = settings.SMTP_USER
        email_message["To"] = send_to

        email_message.set_content(text)

        return email_message

    def send_message(self, message: EmailMessage) -> None:
        with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(message)