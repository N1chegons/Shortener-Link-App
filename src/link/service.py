import json

from src.database import async_session
from src.link.exceptions import SlugAlreadyExistsError
from src.link.repository import add_short_url_to_database, check_short_url_already
from src.link.utilits import generate_random_short_url, hash_url, redis_client


async def generate_short_url(
        long_url: str
) -> str:

    url_hash = hash_url(long_url)
    redis_key = f"url:{url_hash}"

    # Проверяем Redis
    cached = await redis_client.get(redis_key)
    if cached:
        return json.loads(cached)['short_url']

    async with async_session() as session:
        already_url = await check_short_url_already(long_url)
        if already_url:
            await redis_client.setex(
                redis_key,
                1800,
                json.dumps({"short_url": already_url, "original_url": long_url})
            )
            return already_url
        else:
            async def _generate_short_url_and_add_to_db() -> str:
                slug = generate_random_short_url()
                await add_short_url_to_database(
                    slug, long_url
                )
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
        return slug