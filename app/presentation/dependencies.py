from fastapi import Request

from app.domain.interfaces import InterfaceCache, InterfaceTextExtractor, InterfaceMessageSender, InterfaceHashGetter
from app.infrastructure.cache import RedisCache
from app.infrastructure.hash_getter import HashGetter
from app.infrastructure.message_sender import SMTPMessageSender
from app.infrastructure.text_extractor import TesseractTextExtractor


def get_cache(request: Request) -> InterfaceCache:
    redis = request.app.state.redis
    return RedisCache(redis)

def get_text_extractor() -> InterfaceTextExtractor:
    return TesseractTextExtractor()

def get_message_sender() -> InterfaceMessageSender:
    return SMTPMessageSender()

def get_hash_getter() -> InterfaceHashGetter:
    return HashGetter()