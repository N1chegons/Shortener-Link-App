from typing import Annotated

from fastapi import APIRouter, status, Body
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from src.link.exceptions import SlugAlreadyExistsError, NoLongUrlFoundError
from src.link.repository import get_original_url_by_short_url
from src.link.service import generate_short_url



router = APIRouter(
    prefix="/shortener",
    tags=["Shortener"]
)


@router.get("/{short_url}", description="В этом эндпоинте можете вписать короткий URL который вы получили при вводе длинной ссылке и получите на выходе готовый URL адресс на сайт. Пример: QweW22.")
async def redirect_to_url(short_url: str):
        try:
            long_url = await get_original_url_by_short_url(short_url)
        except NoLongUrlFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не существует")
        return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)

@router.post("/get_short_url", description="В этом эндпоинте можете вписать ссылку на сайт, у которого хотите скоратить URL.")
async def get_short_url(long_url: Annotated[str, Body(embed=True)]):
    try:
        new_short_url = await generate_short_url(long_url)
    except SlugAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't generate short url."
        )
    return {"New short url": new_short_url}
