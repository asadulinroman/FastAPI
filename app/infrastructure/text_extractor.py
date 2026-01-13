import asyncio
from pytesseract import image_to_string
from PIL import Image

from app.domain.interfaces import InterfaceTextExtractor

class TesseractTextExtractor(InterfaceTextExtractor):
    async def extract_text(self, file_path: str, language: str) -> str:
        def extract():
            with Image.open(file_path) as image:
                return image_to_string(image, language)
        return await asyncio.to_thread(extract)