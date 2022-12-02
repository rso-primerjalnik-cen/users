from fastapi import FastAPI

from app.api.routers import users
from app.common.settings import get_settings

fastapi_app = FastAPI()

settings = get_settings()

API_PREFIX = '/api/v1'
fastapi_app.include_router(users.router, prefix=API_PREFIX)
