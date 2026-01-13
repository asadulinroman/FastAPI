from pydantic import EmailStr
from fastapi import Depends

from app.application.services import SendMessageToEmailService
from app.infrastructure.celery.celery_app import celery
from app.presentation.dependencies import get_message_sender


@celery.task
def send_message_to_email_task(
        email: EmailStr,
        extracted_text: str,
):
    email_sender = get_message_sender()
    service = SendMessageToEmailService(email_sender)
    service.send_email(email, extracted_text)