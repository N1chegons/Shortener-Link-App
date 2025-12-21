from fastapi import APIRouter, Depends, Query, Request
from fastapi_cache import default_key_builder

from src.auth.repository import UserRepository
from src.auth.router import cur_user
from src.auth.models import User

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

@router.get("/get_my_favlinks")
async def get_favorite_links(
    user: User = Depends(cur_user)
):
    links = await UserRepository.get_my_favorite_links(user.id)
    return {
        "user": user.email,
        "favorite links": links,
    }

@router.post("/add_favlinks")
async def add_favorite_link(short_url: str = Query(max_length=6, min_length=6), user: User = Depends(cur_user)):
    new_favlink = await UserRepository.add_to_my_favorite_links(short_url, user.id)
    return new_favlink
# @router.get("/", summary="Profile")
# async def get_profile_rep(user: User = Depends(cur_user)):
#     async with async_session() as session:
#         query = select(User).filter_by(id=user.id)
#         result = await session.execute(query)
#         calc = result.unique().scalars().all()
#         alr = [ProfileRead.model_validate(p) for p in calc]
#         # noinspection PyBroadException
#         try:
#             if user.is_superuser:
#                 return {
#                     "status": 200,
#                     "Role": "Administrator",
#                     "Profile": alr,
#                 }
#             return {
#                 "status": 200,
#                 "Profile": alr,
#             }
#         except:
#             return {"status": 204, "message": "Unknown error"}
