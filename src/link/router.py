from typing import Annotated

from pydantic import HttpUrl
from fastapi import APIRouter, status, Body, Response
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from src.link.exceptions import SlugAlreadyExistsError, NoLongUrlFoundError
from src.link.service import get_original_url_by_short_url

from src.link.utilits import generate_short_url, generate_qr_by_short_url
from src.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)
router = APIRouter(
    prefix="/shortener",
    tags=["Shortener"]
)


@router.get("/{short_url}", description="В этом эндпоинте можете вписать короткий URL который вы получили при вводе длинной ссылке и получите на выходе готовый URL адресс на сайт. Пример: QweW22.")
async def redirect_to_url(short_url: str):
        logger.info(f"Запрос на переадресацию по короткой ссылке: {short_url}")
        long_url = await get_original_url_by_short_url(short_url)
        logger.info(f"Нахождение оригинальной ссылки по короткой ссылки {short_url}: {long_url}")
        if long_url:
            logger.info(f"Успешная переадресацию по {short_url}")
            return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
        else:
            logger.error(f"Не удалось найти оригинальную ссылку по короткой ссылке -> {short_url}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не существует")



@router.get("/get_qr_by_short_url/{short_url}")
async def get_qr_code_short_url(short_url: str):
    logger.info(f"Запрос на создание QR по короткой ссылке: {short_url}")
    try:
        logger.info(f"Успешное создание QR по короткой ссылке -> {short_url}")
        return await generate_qr_by_short_url(short_url)
    except Exception:
        logger.error(f"Ошибка сервера."
                       f"status: 500."
                       f" detail: Не получается сгенерировать QRcode.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не получается сгенерировать QRcode."
        )

@router.post("/get_short_url", description="В этом эндпоинте можете вписать ссылку на сайт, у которого хотите скоратить URL.")
async def get_short_url(long_url: Annotated[HttpUrl, Body(embed=True)]):
    logger.info(f"Запрос на создание короткой сслыки по оригинальной ссылке: {long_url}")
    try:
        new_short_url = await generate_short_url(str(long_url))
        logger.info(f"Успешное создание короткой ссылки. {long_url} -> {new_short_url}")
    except SlugAlreadyExistsError:
        logger.error(f"Ошибка сервера."
                       f"status: 500."
                       f"detail: Не получается сгенерировать url.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не получается сгенерировать url."
        )
    logger.info(f"Отправка пользовтелю короткую ссылку: {new_short_url}")
    return {"New short url": new_short_url}