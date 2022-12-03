from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from app.api.routers import users
from app.common.auth import KeycloakOpenIDAuthBackend, on_auth_error
from app.common.settings import get_settings

fastapi_app = FastAPI()

settings = get_settings()

fastapi_app.add_middleware(AuthenticationMiddleware, backend=KeycloakOpenIDAuthBackend(), on_error=on_auth_error)

API_PREFIX = '/api/v1'
fastapi_app.include_router(users.router, prefix=API_PREFIX)
