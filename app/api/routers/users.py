from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/user_id')
async def get_user_profile(user_id: str):
    return f'{user_id}'
