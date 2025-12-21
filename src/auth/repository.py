from typing import List

from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.exceptions import HTTPException

from src.database import async_session
from src.link.models import FavoriteLink
from src.link.repository import get_original_url_by_short_url
from src.link.scheams import FavoriteLinkView


async def _get_fav_link(user_id: int, short_url: str):
    async with async_session() as session:
        query = select(FavoriteLink).where(
            FavoriteLink.user_id == user_id,
            FavoriteLink.short_url == short_url
        )
        result = await session.execute(query)
        return result.scalars().first()

class UserRepository:
    @classmethod
    async def get_my_favorite_links(cls, user_id: int):
        async with async_session() as session:
            query = (
                select(FavoriteLink)
                .filter_by(user_id=user_id)
                .order_by(FavoriteLink.id)
                .options(joinedload(FavoriteLink.link))
            )
            result = await session.execute(query)
            favlinks = [FavoriteLinkView.model_validate(el) for el in result.scalars().all()]
            return favlinks

    @classmethod
    async def add_to_my_favorite_links(cls, short_url: str,  user_id: int):
        async with async_session() as session:
            link = await get_original_url_by_short_url(short_url)
            if not link:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Url не найден."
                )

            existing = await _get_fav_link(user_id, short_url)
            if existing:
                return {"message":f"url {short_url} уже добавлен в избранное."}

            stmt = insert(FavoriteLink).values(user_id=user_id, short_url=short_url).returning(FavoriteLink)
            mew_favlink = await session.execute(stmt)
            try:
                await session.commit()
                return {"message": "Ссылка добавлена в избранное."}
            except Exception:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Что-то пошло не так.")