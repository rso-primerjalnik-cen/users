from fastapi import APIRouter, Request, HTTPException
from starlette import status

from app.api.serializers.users import UpdateUserProfile
from app.common.settings import get_settings
from app.common.users.repository import KeycloakUsersRepository
from app.common.users.utils import to_keycloak_user

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/health/live/')
async def health_check_liveness():
    s = get_settings()
    liveness_check = s.get_liveness_check()
    if liveness_check == 'bad':
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Liveness check failed')
    return dict(status='OK')


@router.get('/health/ready/')
async def health_check_readiness():
    repo = KeycloakUsersRepository()
    try:
        repo.get_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    return dict(status='OK')


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


@router.patch('/profile/{user_id}/')
async def update_user(user_id: str, request: Request, user_data: UpdateUserProfile):
    user_repo: KeycloakUsersRepository = KeycloakUsersRepository()
    user = await user_repo.update_user(user_id=user_id, user=to_keycloak_user(user_data.dict()))

    return dict(id=user.id,
                username=user.preferred_username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                email_verified=user.email_verified,
                country=user.country,
                date_of_birth=user.date_of_birth
                )


@router.put('/profile/{user_id}/email/')
async def update_user_email(user_id: str, request: Request, user_data: UpdateUserProfile):
    user_repo: KeycloakUsersRepository = KeycloakUsersRepository()
    user = await user_repo.update_user(user_id=user_id, user=to_keycloak_user(user_data.dict()))

    return dict(id=user.id,
                username=user.preferred_username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                email_verified=user.email_verified,
                country=user.country,
                date_of_birth=user.date_of_birth
                )
