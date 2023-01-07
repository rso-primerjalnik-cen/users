import json
from datetime import datetime
from typing import Optional, List

from pydantic import ValidationError
from starlette import status

from app.api.exceptions import AttrValidationHTTPException
from app.common.settings import get_settings
from app.common.users.managers import KeycloakManager

from app.common.users.models import KeycloakUser
from app.common.users.utils import to_keycloak_user, from_keycloak_user


class KeycloakUsersRepository(object):
    _client = None
    _keycloak = None

    def add(self, model, *args, **kwargs) -> str:
        pass

    @property
    def config(self) -> dict:
        settings = get_settings()
        return dict(HOST=settings.get_keycloak_api(),
                    ADMIN_USER=settings.get_keycloak_admin_user(),
                    ADMIN_SECRET=settings.get_keycloak_admin_secret(),
                    REALM_NAME=settings.get_keycloak_realm(),
                    CLIENT_ID=settings.get_keycloak_client_id(),
                    CLIENT_SECRET_KEY=settings.get_keycloak_client_secret_key(),
                    REDIRECT_URL=settings.get_keycloak_redirect_url(),
                    SSL_VERIFY=settings.get_keycloak_ssl_verify())

    @property
    def keycloak(self) -> KeycloakManager:
        if not self._keycloak:
            self._keycloak = KeycloakManager(realm=self.config.get('REALM_NAME'), config=self.config)

        self._keycloak.refresh_token()
        return self._keycloak

    @property
    async def client(self) -> dict:
        return self.keycloak.client

    @property
    async def client_id(self) -> str:
        client = await self.client
        return client.get('id')

    async def get_user(self, user_id: str) -> KeycloakUser:
        return to_keycloak_user(await self.get_user_raw(user_id))

    async def get_user_raw(self, user_id: str) -> dict:
        return self.keycloak.get_user(user_id)

    def delete_user(self, user_id: str):
        self.keycloak.delete_user(user_id)

    def get_users(self, **kwargs) -> List[KeycloakUser]:
        return [to_keycloak_user(user) for user in self.keycloak.get_users(kwargs)]

    def first(self, *args, **kwargs) -> Optional[KeycloakUser]:
        users = self.keycloak.get_users(kwargs)
        return to_keycloak_user(users[0]) if users else None

    def exists(self, *args, **kwargs) -> bool:
        return self.first(*args, **kwargs) is not None

    async def update_user(self, user_id: str, user: KeycloakUser) -> KeycloakUser:
        existing_user = to_keycloak_user(self.keycloak.get_user(user_id=user_id))

        email_changed = (existing_user.email != user.email) if user.email else False

        existing_user = from_keycloak_user(existing_user)

        user.modified_on = datetime.now()
        user = from_keycloak_user(user)

        # Only passing changed user attributes overwrites all already saved attributes.
        # Therefore, we have to change/add attributes of an existing instance of a keycloak user,
        # instead of just passing updated attributes.
        if not user['enabled']:
            existing_user['enabled'] = False
        self.update_user_info(src=user, dest=existing_user)
        self.update_user_attributes(src=user, dest=existing_user)

        try:
            if existing_user['id']:
                if email_changed:
                    existing_user['emailVerified'] = False
                self.keycloak.update_user(existing_user['id'], existing_user)
            else:
                user.id = self.keycloak.create_user(user)
        except Exception as e:
            if len(e.args):
                string_msg = e.args[0].decode('utf-8') if isinstance(e.args[0], bytes) else e.args[0]
                msg = json.loads(string_msg)['errorMessage']
                raise AttrValidationHTTPException(status_code=status.HTTP_400_BAD_REQUEST, attr='email', attr_error=msg)
            else:
                raise e

        if email_changed:
            self.send_verify_email(existing_user['id'])
        return to_keycloak_user(existing_user)

    def update_user_info(self, src: dict, dest: dict):
        for key, value in {k: v for k, v in src.items() if v}.items():
            if key != 'attributes':
                dest[key] = value

    def update_user_attributes(self, src: dict, dest: dict):
        for key, value in {k: v for k, v in src['attributes'].items() if v}.items():
            dest['attributes'][key] = value

    async def create_user(self, **user_data) -> KeycloakUser:
        recaptcha = user_data.pop('recaptcha', None)
        password = user_data.pop('password', None)
        password2 = user_data.pop('password2', None)

        user = KeycloakUser(**user_data)
        user_data_dict = from_keycloak_user(user)
        user_data_dict['credentials'] = [{"value": password, "type": "password", }]
        user.id = self.keycloak.create_user(user_data_dict, exist_ok=False)

        if user.email:
            self.send_verify_email(user_id=user.id)

        return user

    def set_password(self, user_id: str, password: str):
        self.keycloak.set_user_password(user_id=user_id,
                                        password=password,
                                        temporary=False)

    def send_verify_email(self, user_id: 'str'):
        self.keycloak.send_verify_email(user_id=user_id,
                                        client_id=self.config.get('CLIENT_ID') + '_public',
                                        redirect_uri=self.config.get('REDIRECT_URL'))

    def execute_actions_email(self, user_id: str, payload: List[str]) -> bool:
        data_raw = self.keycloak.raw_put(f"{self.config.get('HOST')}admin/realms/{self.config.get('REALM_NAME')}/users/{user_id}/execute-actions-email", data=json.dumps(payload))
        return data_raw.status_code == 204

    def get_credentials(self, user_id):
        data_raw = self.keycloak.raw_get(f"{self.config.get('HOST')}admin/realms/{self.config.get('REALM_NAME')}/users/{user_id}/credentials", data=None)
        return json.loads(data_raw.content)

    def remove_otp(self, user_id: str, credential_id: str) -> bool:
        data_raw = self.keycloak.raw_delete(f"{self.config.get('HOST')}admin/realms/{self.config.get('REALM_NAME')}/users/{user_id}/credentials/{credential_id}/", data=None)
        return data_raw.status_code == 204
