from datetime import datetime
from enum import Enum

from starlette.authentication import BaseUser


class WithdrawConfirmationMethod(str, Enum):
    OTP = 'otp'
    EMAIL = 'email'


class KeycloakUser(BaseUser):
    # Keycloak OpenID attributes - these will be available in request.user model
    name: str
    family_name: str
    given_name: str
    preferred_username: str
    sub: str
    email_verified: bool = False

    # Other Keycloak attributes - available when we get user data from KeycloakManager
    email: str
    phone: str
    address: str
    country: dict
    ewallet_id: str
    date_of_birth: str
    enabled: bool = True
    # Timestamp in milliseconds
    created_timestamp: int
    kyc_status: str
    dob: str

    # Custom Keycloak attributes - added by us - also available when we get user from KeycloakManager
    modified_on: datetime

    # Withdrawal confirmation method
    withdrawal_confirmation_method: WithdrawConfirmationMethod = WithdrawConfirmationMethod.OTP
    kyc_info: str

    def __init__(self, **user_data):
        for key in user_data:
            setattr(self, key, user_data.get(key))

    # Properties used by Authentication Middleware
    @property
    def is_authenticated(self) -> bool:
        # In case user authentication fails we raise exception so this attribute doesn't really matter
        return True

    @property
    def display_name(self) -> str:
        return self.preferred_username

    @property
    def identity(self) -> str:
        return self.preferred_username

    # Properties added just for convenience since keycloak attribute naming can be confusing
    @property
    def username(self) -> str:
        return self.preferred_username

    @username.setter
    def username(self, value: str):
        self.preferred_username = value

    # In keycloak id == uuid
    @property
    def id(self) -> str:
        return self.sub

    @id.setter
    def id(self, value: str):
        self.sub = value

    @property
    def first_name(self) -> str:
        return self.given_name

    @first_name.setter
    def first_name(self, value: str):
        self.given_name = value

    @property
    def last_name(self) -> str:
        return self.family_name

    @last_name.setter
    def last_name(self, value: str):
        self.family_name = value

    @property
    def created_on(self) -> datetime:
        # created_timestamp = timestamp in milliseconds instead of seconds
        return datetime.fromtimestamp(self.created_timestamp / 1000)

    # some attributes could be undefined at first, avoid exceptions for those
    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            if item in self.__annotations__:
                return None
            raise e
