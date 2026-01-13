import hashlib

from app.domain.interfaces import InterfaceHashGetter
import aiofiles

class HashGetter(InterfaceHashGetter):

    async def get_hash(self, file_path: str) -> str:
        async with aiofiles.open(file_path, 'rb') as file:
            content = await file.read()
            file_hash = hashlib.md5(content).hexdigest()
            return file_hash

