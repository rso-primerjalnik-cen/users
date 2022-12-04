import json

from fastapi import APIRouter, Request

from app.common.users.repository import KeycloakUsersRepository

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users(request: Request):
    # repo = KeycloakUsersRepository()
    # return repo.get_users()
    return json.loads('[{"sub":"62d815ad-1d3d-4bb0-8da9-bdec18e38949","created_timestamp":1670099542243,"preferred_username":"keycloak_admin","enabled":true,"totp":false,"email_verified":false,"disableable_credential_types":[],"required_actions":[],"not_before":0,"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}},{"sub":"abecf261-42ca-4208-937c-e39a2f0d53c0","created_timestamp":1670031475897,"preferred_username":"lan","enabled":true,"totp":false,"email_verified":false,"given_name":"Lan","family_name":"Strlic","email":"lan.strlic@gmail.com","disableable_credential_types":[],"required_actions":[],"not_before":0,"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}},{"sub":"386d314f-a95f-405f-925f-37f735dfd6a5","created_timestamp":1670160190374,"preferred_username":"mare","enabled":true,"totp":false,"email_verified":false,"given_name":"Marko","family_name":"Meki","email":"marko@marko.com","disableable_credential_types":[],"required_actions":[],"not_before":0,"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}},{"sub":"bb9d0d01-3d4b-4981-8577-d5336b2836a6","created_timestamp":1670160130588,"preferred_username":"testuser","enabled":true,"totp":false,"email_verified":false,"given_name":"Test","family_name":"Testić","email":"test@example.com","disableable_credential_types":[],"required_actions":[],"not_before":0,"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}},{"sub":"51860b9e-668d-477a-9609-fa43aeee7ed7","created_timestamp":1670160254509,"preferred_username":"timi","enabled":true,"totp":false,"email_verified":false,"given_name":"Timotej","family_name":"Strlic","email":"tim@tim.com","disableable_credential_types":[],"required_actions":[],"not_before":0,"access":{"manageGroupMembership":true,"view":true,"mapRoles":true,"impersonate":true,"manage":true}}]')


@router.get('/profile/')
async def get_user_profile(request: Request):
    user_repo: KeycloakUsersRepository = KeycloakUsersRepository()
    user = await user_repo.get_user(request.user.id)
    return dict(id=user.id,
                username=user.preferred_username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                email_verified=user.email_verified,
                country=user.country,
                date_of_birth=user.date_of_birth)
