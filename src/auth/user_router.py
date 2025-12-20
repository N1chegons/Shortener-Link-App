from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy import select, update

from src.database import async_session
from src.auth.models import User

router = APIRouter(
    tags=["User"],
    prefix="/profile"
)


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
