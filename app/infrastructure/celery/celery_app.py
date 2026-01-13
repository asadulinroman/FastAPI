from celery import Celery
from app.config import settings

celery = Celery(
    'email_sender',
    broker=settings.BROKER_URL,
    include=['app.infrastructure.celery.tasks'],
)
