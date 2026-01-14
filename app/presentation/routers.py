import os
from fastapi import APIRouter, Depends

from app.domain.interfaces import InterfaceCache, InterfaceTextExtractor, InterfaceHashGetter, InterfaceMessageSender
from app.domain.schemas import AnalyzeDocShema, SendMessageToEmailSchema
from app.application.services import AnalyzeDocService

from app.infrastructure.celery.tasks import send_message_to_email_task
from app.presentation.dependencies import get_cache, get_text_extractor, get_hash_getter, get_message_sender

router = APIRouter(
    prefix="",
    tags=["Получение текста с изображения и отправка на почту"],
)

@router.post("/analyze_doc")
async def extract_text(request: AnalyzeDocShema,
                       cache: InterfaceCache = Depends(get_cache),
                       text_extractor: InterfaceTextExtractor = Depends(get_text_extractor),
                       hash_getter: InterfaceHashGetter = Depends(get_hash_getter),
                       ):
    filename = request.filename
    file_path = os.path.join("/app/media/images", filename)
    service = AnalyzeDocService(cache, text_extractor, hash_getter)
    return await service.analyze_doc(file_path)

@router.post("/send_message_to_email")
async def send_message_to_email(request: SendMessageToEmailSchema):
    email = request.email
    extracted_text = request.extracted_text
    send_message_to_email_task.delay(email,extracted_text)
    return {'publish': 'OK'}

@router.get("/health_check")
async def health_check():
    return {{
        {'status': True}
        
    }}