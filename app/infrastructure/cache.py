from redis.asyncio import Redis

from app.domain.interfaces import InterfaceCache

class RedisCache(InterfaceCache):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, cache_key: str) -> str:
        return await self.redis.get(cache_key)

    async def set(self, cache_key: str, expire: int, value: str) -> None:
        await self.redis.setex(cache_key, expire, value)