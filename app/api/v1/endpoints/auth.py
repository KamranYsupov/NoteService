import jwt
from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.services.jwt import JWTService, TokenEnum
from ..deps import validate_auth_user, get_current_user_refresh, get_current_user_access
from app.core.container import Container
from app.db import User
from app.schemas.auth import TokenInfoSchema

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenInfoSchema,
)
@inject
async def auth_user(
        user: User = Depends(validate_auth_user),
        jwt_service: JWTService = Depends(Provide[Container.jwt_service])
) -> TokenInfoSchema:
    access_token = await jwt_service.encode(user=user, token_type=TokenEnum.ACCESS)
    refresh_token = await jwt_service.encode(user=user, token_type=TokenEnum.REFRESH)

    token_info = TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )

    return token_info


@router.post('/logout', status_code=status.HTTP_200_OK)
@inject
async def logout_user(
        user: User = Depends(get_current_user_access),
        jwt_service: JWTService = Depends(Provide[Container.jwt_service])
) -> None:
    await jwt_service.logout(sub=user.id)


@router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    response_model=TokenInfoSchema,
    response_model_exclude_none=True,
)
@inject
async def refresh_access_token(
        user: User = Depends(get_current_user_refresh),
        jwt_service: JWTService = Depends(Provide[Container.jwt_service])
) -> TokenInfoSchema:
    access_token = await jwt_service.encode(user=user, token_type=TokenEnum.ACCESS)

    token_info = TokenInfoSchema(
        access_token=access_token,
    )

    return token_info


