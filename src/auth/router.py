from fastapi import Depends, APIRouter
from fastapi_users import FastAPIUsers
from pydantic import EmailStr
from sqlalchemy import select, update

from src.auth.config import auth_backend
from src.auth.manager import get_user_manager
from src.database import async_session
from src.auth.models import User

from src.auth.schemas import UserRead, UserCreate

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

# conf fastapi_users
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


cur_user = fastapi_users.current_user()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset_password",
)