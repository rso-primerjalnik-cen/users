from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import users
from app.common.auth import KeycloakOpenIDAuthBackend, on_auth_error
from app.common.settings import get_settings

API_PREFIX = '/api/v1'

fastapi_app = FastAPI(docs_url=f"{API_PREFIX}/users/docs")

settings = get_settings()

fastapi_app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"])

fastapi_app.add_middleware(AuthenticationMiddleware, backend=KeycloakOpenIDAuthBackend(), on_error=on_auth_error)

GRAPHQL_PREFIX = '/api/v1/users/graphql'
fastapi_app.include_router(users.router, prefix=API_PREFIX)
fastapi_app.include_router(users.graphql_router, prefix=GRAPHQL_PREFIX)
