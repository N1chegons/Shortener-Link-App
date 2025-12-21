from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware

from src.config import settings

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="Link Shortener",
    summary="In this project, you can shorten links using this API.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def get_home_page():
    return {
        "status": 200,
        "message": "Hello"
    }

from src.auth.router import router as auth_router
from src.link.router import router
from src.auth.user_router import router as user_router

app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)