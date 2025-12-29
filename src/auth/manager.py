from typing import Optional, Dict

import resend
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager,IntegerIDMixin

from src.auth.models import User
from src.config import settings
from src.database import get_user_db
from src.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)
SECRET = settings.MANAGER_PASS
resend.api_key=settings.RESEND_API_KEY

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {User.id} has registered. Data: email - {user.email}, is_active - {user.is_active}")

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ):
        logger.info(f"User has logged in system. Data: email - {user.email}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        params: resend.Emails.SendParams = {
            "from": "shortenerapp@petproject.website",
            "to": user.email,
            "subject": "Password reset code",
            "html": f"<h1>Token for resent password:</h1>"
                    f"<p>{token}</p>"
                    f"<p>Don't tell anyone the code.</p>",
        }
        email: resend.Email = resend.Emails.send(params)

        logger.info(f"User {user.id} has forgot their password.\n"
              f"Reset token: {token}")
        return email

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)