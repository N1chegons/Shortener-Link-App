from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from src.config import settings

SECRET = settings.JWT_KEY

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# connect cookie
cookie_transport = CookieTransport(cookie_max_age=3600)

# backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)