from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.exceptions import HTTPException

from src.database import async_session
from src.link.models import FavoriteLink
from src.link.service import get_original_url_by_short_url
from src.link.scheams import FavoriteLinkView
from src.logger import get_logger

logger = get_logger(__name__)


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
                logger.warning(f"Ссылка уже добавлена в избранное: Параметры {short_url} - {user_id}")
                return {"message":f"url {short_url} уже добавлен в избранное."}

            stmt = insert(FavoriteLink).values(user_id=user_id, short_url=short_url).returning(FavoriteLink)
            mew_favlink = await session.execute(stmt)
            try:
                await session.commit()
                logger.info(f"Успешное добавление ссылки в избранное: Парамтеры {short_url} - {user_id}")
                return {"message": "Ссылка добавлена в избранное."}
            except Exception:
                logger.error(f"Ошибка сервера."
                             f"status: 500."
                             f" detail: Что-то пошло не так. Параметры {short_url} - {user_id}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Что-то пошло не так.")


    @classmethod
    async def delete_my_favlink(cls, short_url: str, user_id: int):
        async with async_session() as session:
            link = await _get_fav_link(user_id, short_url)
            query = delete(FavoriteLink).filter_by(short_url=short_url, user_id=user_id)
            if not link:
                logger.warning(f"Ссылка не находится в избранном или не существует: Параметры {short_url} - {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ссылка не существует либо не находится у вас в избранном."
                )

            await session.execute(query)
            try:
                await session.commit()
                logger.info(f"Успешное удаление ссылки из избранного: Парамтеры {short_url} - {user_id}")
                return {
                    "status": status.HTTP_200_OK,
                    "message": f"Ссылка {short_url} удалена из избранного.",
                }
            except:
                logger.error(f"Ошибка сервера."
                             f"status: 500."
                             f" detail: Что-то пошло не так. Параметры {short_url} - {user_id}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Что-то пошло не так.")
