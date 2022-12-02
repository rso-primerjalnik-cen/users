import re
from datetime import datetime

from dateutil import parser

from app.common.users.models import KeycloakUser


def camel_to_snake(value: 'str') -> 'str':
    """
    Convert value from camelCase to snake_case
    :param value: Camel case value
    :return: Snake case value
    """
    return re.sub('(?!^)([A-Z]+)', r'_\1', value).lower()


def snake_to_camel(value: 'str') -> 'str':
    """
    Convert value from snake_case to camelCase
    :param value: Snake case value
    :return: Camel case value
    """
    words = value.split('_')
    return words[0] + ''.join(w.title() for w in words[1:])


def to_keycloak_user(user: 'dict') -> 'KeycloakUser':
    _user = {camel_to_snake(key): value for key, value in user.items()}
    keycloak_user = KeycloakUser(**_user)

    attributes = user.get('attributes')
    if attributes:
        for key in attributes:
            attribute = attributes[key]
            snake_case_key = camel_to_snake(key)
            if attribute and isinstance(attribute, list) and len(attribute) == 1:
                attribute = attribute[0]
            attribute_type = KeycloakUser.__annotations__.get(snake_case_key)
            if attribute_type == 'datetime':
                attribute = parser.parse(attribute)
            setattr(keycloak_user, snake_case_key, attribute)

    return keycloak_user


def from_keycloak_user(user: 'KeycloakUser') -> 'dict':
    ignore_attributes = [
        # OpenID attributes
        'sub', 'preferred_username', 'given_name', 'family_name', 'name',
        # properties used by Authentication Middleware
        'is_authenticated', 'display_name', 'identity',
        # other Keycloak attributes that should be read-only
        'created_timestamp', 'not_before', 'totp', 'disableable_credential_types', 'required_actions', 'access',
        'created_on'
    ]

    # Keycloak User Representation for JSON fields:
    # https://www.keycloak.org/docs-api/12.0/rest-api/index.html#_userrepresentation
    # Use this attributes to identify custom attributes that we added to KeycloakUser model
    keycloak_user_representation_attrs = ['access', 'attributes', 'clientConsents', 'clientRoles', 'createdTimestamp',
                                          'credentials', 'disableableCredentialTypes', 'email', 'emailVerified',
                                          'enabled', 'federatedIdentities', 'federationLink', 'firstName', 'groups',
                                          'id', 'lastName', 'notBefore', 'origin', 'realmRoles', 'requiredActions',
                                          'self', 'serviceAccountClientId', 'username']

    user_dict = dict(attributes=dict())
    user_class_properties = dir(user)
    user_class_properties = [cp for cp in user_class_properties
                             if cp not in ignore_attributes and not cp.startswith('__') and not callable(cp)]
    for cp in user_class_properties:
        attr = getattr(user, cp)
        if isinstance(attr, datetime):
            attr = str(attr)
        camel_case_attr = snake_to_camel(cp)
        if camel_case_attr in keycloak_user_representation_attrs:
            user_dict[camel_case_attr] = attr
        else:
            user_dict['attributes'][camel_case_attr] = attr
    return user_dict
