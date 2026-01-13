import pytest

from app.infrastructure.cache import RedisCache

@pytest.mark.anyio
async def test_redis_cache_get(mocker):
    mock_redis = mocker.AsyncMock()

    cache = RedisCache(mock_redis)
    cache_key = "test_key"
    cache_value = "test_value"
    mock_redis.get.return_value = cache_value

    result = await cache.get(cache_key)

    assert result == cache_value
    mock_redis.get.assert_awaited_once_with(cache_key)

@pytest.mark.anyio
async def test_redis_cache_set(mocker):
    mock_redis = mocker.AsyncMock()

    cache = RedisCache(mock_redis)
    cache_key = "test_key"
    expire = 3600
    cache_value = "test_value"

    await cache.set(cache_key, expire, cache_value)

    mock_redis.setex.assert_awaited_once_with(cache_key, expire, cache_value)