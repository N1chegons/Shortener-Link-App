import io
import string
import hashlib
import json
import segno
from secrets import choice

from fastapi import Response
from src.database import async_session
from src.link.exceptions import SlugAlreadyExistsError
from src.link.service import add_short_url_to_database, check_short_url_already, get_original_url_by_short_url

from fastapi_cache.backends import redis
from src.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)
ALPHABET: str = string.ascii_letters + string.digits
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def generate_random_short_url() -> str:
    slug = ""
    for _ in range(6):
        slug += choice(ALPHABET)
    logger.info(f"Короткая ссылка сгенерировона: {slug}")
    return slug

def hash_url(url: str) -> str:
    url = url.lower().strip()
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    if url.startswith('www.'):
        url = url[4:]

    logger.info(f"URL захеширован:{url} -> {hashlib.md5(url.encode()).hexdigest()}")
    return hashlib.md5(url.encode()).hexdigest()

async def generate_short_url(
        long_url: str
) -> str:
    logger.info(f"Генерация и добавление короткой ссылки по оригинальной ссылки: {long_url}.")
    url_hash = hash_url(long_url)
    redis_key = f"url:{url_hash}"

    cached = await redis_client.get(redis_key)
    if cached:
        logger.info(f"Ссылка вернулась из Redis: {json.loads(cached)['short_url']}")
        return json.loads(cached)['short_url']

    async with async_session() as session:
        already_url = await check_short_url_already(long_url)
        if already_url:
            await redis_client.setex(
                redis_key,
                1800,
                json.dumps({"short_url": already_url, "original_url": long_url})
            )
            logger.info(f"Вернули ссылку -> {already_url}, а также добавлили в Redis.")
            return already_url
        else:
            async def _generate_short_url_and_add_to_db() -> str:
                slug = generate_random_short_url()
                await add_short_url_to_database(
                    slug, long_url
                )
                logger.info(f"Сгенерировали короткую ссылку и добавили в базу данных: {slug} - {long_url}")
                return slug

            for attempt in range(5):
                try:
                    slug = await _generate_short_url_and_add_to_db()
                    await redis_client.setex(
                        redis_key,
                        1800,
                        json.dumps({"short_url": slug, "original_url": long_url})
                    )
                    return slug
                except SlugAlreadyExistsError as ex:
                    if attempt == 4:
                        raise SlugAlreadyExistsError from ex

        logger.info(f"Успешное отдача короткой ссылки: {slug}")
        return slug

async def generate_qr_by_short_url(short_url: str):
    logger.info(f"Создание QR по -> {short_url}")
    original_url = await get_original_url_by_short_url(short_url)
    logger.info(f"Венулось с поиска оригинальной ссылки: {short_url} -> {original_url}")
    qr = segno.make(original_url)

    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=5)
    buffer.seek(0)

    logger.info(f"Успешное создание QR кода по: {short_url}")
    return Response(
        content=buffer.getvalue(),
        media_type="image/png"
    )

