from abc import ABC, abstractmethod
from typing import Optional

class InterfaceCache(ABC):
    @abstractmethod
    async def get(self, cache_key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, cache_key: str, expire: int, value: str) -> None:
        pass

class InterfaceMessageSender(ABC):
    @abstractmethod
    async def create_message(self, send_to: object, text: str) -> object:
        pass

    @abstractmethod
    def send_message(self, message: object) -> None:
        pass

class InterfaceTextExtractor(ABC):
    @abstractmethod
    async def extract_text(self, file_path: str, language: str) -> str:
        pass

class InterfaceHashGetter(ABC):
    @abstractmethod
    async def get_hash(self, file_path: str) -> str:
        pass