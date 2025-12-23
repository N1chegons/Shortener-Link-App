from fastapi import APIRouter, Depends

from src.auth.repository import UserRepository
from src.auth.models import User
from src.auth.router import fastapi_users

router = APIRouter(
    tags=["User"],
    prefix="/user"
)
cur_user = fastapi_users.current_user()

@router.get("/get_my_favlinks")
async def get_favorite_links(
    user: User = Depends(cur_user)
):
    links = await UserRepository.get_my_favorite_links(user.id)
    return {
        "user": user.email,
        "favorite links": links,
    }

@router.post("/add_favlinks/{short_url}")
async def add_favorite_link(short_url: str, user: User = Depends(cur_user)):
    new_favlink = await UserRepository.add_to_my_favorite_links(short_url, user.id)
    return new_favlink

@router.delete("/delete_favlink/{short_url}")
async def delete_favorite_link(short_url: str, user: User = Depends(cur_user)):
    deleted_favlink = await UserRepository.delete_my_favlink(short_url, user.id)
    return deleted_favlink