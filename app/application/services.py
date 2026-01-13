from pydantic import EmailStr

from app.domain.interfaces import InterfaceCache, InterfaceTextExtractor, InterfaceMessageSender, InterfaceHashGetter


class AnalyzeDocService:
    def __init__(self, cache: InterfaceCache, text_extractor: InterfaceTextExtractor, hash_getter: InterfaceHashGetter):
        self.cache = cache
        self.text_extractor = text_extractor
        self.hash_getter = hash_getter

    async def analyze_doc(self, file_path: str) -> dict:
        cache_key = await self.hash_getter.get_hash(file_path)
        cached = await self.cache.get(cache_key)
        if cached:
            return {"text": cached, "from_cache": True}

        text = await self.text_extractor.extract_text(file_path, "rus+eng")

        await self.cache.set(cache_key, 3600, text)
        return {"text": text, "from_cache": False}

class SendMessageToEmailService:
    def __init__(self, email_sender: InterfaceMessageSender):
        self.email_sender = email_sender

    def send_email(self, email: EmailStr, extracted_text: str) -> None:
        message = self.email_sender.create_message(email, extracted_text)
        return self.email_sender.send_message(message)