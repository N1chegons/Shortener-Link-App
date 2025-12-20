from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from src.database import async_session
from src.link.exceptions import SlugAlreadyExistsError
from src.link.models import Link


async def check_short_url_already(long_url: str):
    async with async_session() as session:
        query = select(Link).filter_by(original_url=long_url)
        result = await session.execute(query)
        res: Link | None = result.scalar_one_or_none()
        return res.short_url if res is not None else None

async def get_original_url_by_short_url(short_url: str):
    async with async_session() as session:
        query = select(Link).filter_by(short_url=short_url)
        result = await session.execute(query)
        res: Link | None = result.scalar_one_or_none()
        return res.original_url if res is not None else None

async def add_short_url_to_database(short_url: str, long_url: str):
    async with async_session() as session:
        stmt = insert(Link).values(short_url=short_url, original_url=long_url).returning(Link)
        add_trade = await session.execute(stmt)
        try:
            await session.commit()
        except IntegrityError:
            raise SlugAlreadyExistsError

