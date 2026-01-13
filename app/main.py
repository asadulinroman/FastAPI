from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis

from app.config import settings
from app.presentation.exeption_handlers import register_exception_handlers
from app.presentation.routers import router

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        redis = Redis(
            host=settings.CACHE_HOST,
            port=settings.CACHE_PORT,
            decode_responses=True,
        )

        app.state.redis = redis

        yield

        await redis.aclose()

    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(router)
    return app