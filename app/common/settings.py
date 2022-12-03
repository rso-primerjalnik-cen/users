from pydantic import BaseSettings


class Settings(BaseSettings):
    KEYCLOAK_API: str = None
    KEYCLOAK_REALM: str = None
    KEYCLOAK_CLIENT_ID: str = None
    KEYCLOAK_ADMIN_USER: str = None
    KEYCLOAK_ADMIN_SECRET: str = None
    KEYCLOAK_REDIRECT_URL: str = None
    KEYCLOAK_SSL_VERIFY: bool = False
    KEYCLOAK_CLIENT_SECRET_KEY: str = None

    class Config:
        env_file = '.env'


def get_settings() -> Settings:
    return Settings()
