from fastapi import APIRouter, Request

from app.common.users.repository import KeycloakUsersRepository

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users(request: Request):
    repo = KeycloakUsersRepository()
    return repo.get_users()


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
