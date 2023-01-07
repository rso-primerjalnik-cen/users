import re
from typing import Tuple, Optional

from fastapi.requests import HTTPConnection
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from starlette.authentication import AuthCredentials, BaseUser, AuthenticationError, UnauthenticatedUser
from starlette.authentication import AuthenticationBackend
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from app.common.settings import get_settings
from app.common.users.models import KeycloakUser

# Endpoints that don't require authenticated user to access
__auth_allow_any_endpoints = {'/docs', '/openapi.json', '/api/v1/users/'}


def is_endpoint_allow_any(endpoint: str) -> bool:
    """
    Can anyone access this endpoint?
    """
    for _endpoint in __auth_allow_any_endpoints:
        if re.match(_endpoint, endpoint):
            return True
    return False


def mark_endpoint_as_allow_any(endpoint: str):
    __auth_allow_any_endpoints.add(endpoint)


def get_keycloak_openid() -> KeycloakOpenID:
    settings = get_settings()
    return KeycloakOpenID(server_url=settings.get_keycloak_api(),
                          client_id=settings.get_keycloak_client_id(),
                          realm_name=settings.get_keycloak_realm(),
                          client_secret_key=settings.get_keycloak_client_secret_key(),
                          verify=settings.get_keycloak_ssl_verify())


class KeycloakOpenIDAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Optional[Tuple[AuthCredentials, BaseUser]]:
        # if is_endpoint_allow_any(endpoint):
        #     return AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        endpoint = conn.scope.get('path')
        if endpoint in ['/docs', '/openapi.json', '/api/v1/users/']:
            return AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        # Always allow OPTIONS requests, so Nuxt Auth lib and FastAPI CORS middleware can handle CORS properly
        if conn.scope.get('method', None) == 'OPTIONS':
            return AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        auth_header = conn.headers.get('Authorization')
        cookie_header = conn.headers.get('Cookie')      # websockets connections only have a cookie
        if not auth_header:
            if not cookie_header:
                raise AuthenticationError('Authentication token is missing')

        try:
            if auth_header:
                _, token = auth_header.split(' ')
            else:
                auth = next(filter(lambda x: 'auth._token.local' in x, cookie_header.split(' ')))
                _, value = auth.rstrip(';').split('=')
                _, token = value.split('%20')
        # can't split auth token
        except ValueError:
            raise AuthenticationError('Authentication token is missing')

        try:
            keycloak_openid = get_keycloak_openid()
            user = keycloak_openid.userinfo(token)
        except (KeycloakAuthenticationError, KeycloakGetError) as e:
            raise AuthenticationError(e.response_body)
        return AuthCredentials(['authenticated']), KeycloakUser(**user)


def on_auth_error(conn: HTTPConnection, exc: Exception) -> Response:
    return Response(status_code=HTTP_401_UNAUTHORIZED, content=str(exc))
