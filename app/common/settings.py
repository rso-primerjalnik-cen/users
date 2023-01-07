from consul import Consul


class Settings(object):
    KEYCLOAK_API: str = None
    KEYCLOAK_REALM: str = None
    KEYCLOAK_CLIENT_ID: str = None
    KEYCLOAK_ADMIN_USER: str = None
    KEYCLOAK_ADMIN_SECRET: str = None
    KEYCLOAK_REDIRECT_URL: str = None
    KEYCLOAK_SSL_VERIFY: bool = False
    KEYCLOAK_CLIENT_SECRET_KEY: str = None
    CONSUL_HOST = 'my-consul'

    def __init__(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        consul_host = os.getenv('CONSUL_HOST')
        self.CONSUL_HOST = consul_host if consul_host else self.CONSUL_HOST
        self.c = Consul(host=self.CONSUL_HOST)

    def get_keycloak_api(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_API', index=index)
        if data is not None:
            self.KEYCLOAK_API = data['Value'].decode("utf-8")
        return self.KEYCLOAK_API

    def get_keycloak_realm(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_REALM', index=index)
        if data is not None:
            self.KEYCLOAK_REALM = data['Value'].decode("utf-8")
        return self.KEYCLOAK_REALM

    def get_keycloak_client_id(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_CLIENT_ID', index=index)
        if data is not None:
            self.KEYCLOAK_CLIENT_ID = data['Value'].decode("utf-8")
        return self.KEYCLOAK_CLIENT_ID

    def get_keycloak_admin_user(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_ADMIN_USER', index=index)
        if data is not None:
            self.KEYCLOAK_ADMIN_USER = data['Value'].decode("utf-8")
        return self.KEYCLOAK_ADMIN_USER

    def get_keycloak_admin_secret(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_ADMIN_SECRET', index=index)
        if data is not None:
            self.KEYCLOAK_ADMIN_SECRET = data['Value'].decode("utf-8")
        return self.KEYCLOAK_ADMIN_SECRET

    def get_keycloak_redirect_url(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_REDIRECT_URL', index=index)
        if data is not None:
            self.KEYCLOAK_REDIRECT_URL = data['Value'].decode("utf-8")
        return self.KEYCLOAK_REDIRECT_URL

    def get_keycloak_ssl_verify(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_SSL_VERIFY', index=index)
        if data is not None:
            self.KEYCLOAK_SSL_VERIFY = data['Value'].decode("utf-8")
        return self.KEYCLOAK_SSL_VERIFY

    def get_keycloak_client_secret_key(self):
        index = None
        index, data = self.c.kv.get('KEYCLOAK_CLIENT_SECRET_KEY', index=index)
        if data is not None:
            self.KEYCLOAK_CLIENT_SECRET_KEY = data['Value'].decode("utf-8")
        return self.KEYCLOAK_CLIENT_SECRET_KEY


def get_settings() -> Settings:
    return Settings()
