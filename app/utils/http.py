import aiohttp
from fastapi import HTTPException
from starlette import status

from app.core.config import settings
from app.schemas.auth import AuthUserSchema


async def authenticate(auth_schema: AuthUserSchema) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{settings.api_v1_url}/auth/login',
            json=auth_schema.model_dump()
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Ошибка сервера. Попробуйте позже.',
                )
            response_data = await response.json()
            
    return response_data