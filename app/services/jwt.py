import datetime
import enum

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from starlette import status

from app.core.config import settings
from app.db import User, RefreshToken
from app.schemas.user import UserSchema
from app.repositories.refresh import RepositoryRefreshToken
from app.db import RefreshToken


class TokenEnum(enum.Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTService:
    def __init__(
            self,
            repository_refresh_token: RepositoryRefreshToken,
            algorithm: str = settings.algorithm,
            access_expire_minutes: int = settings.access_expire_minutes,
            refresh_expire_days: int = settings.refresh_expire_days,
    ):

        self.algorithm = algorithm
        self.access_expire_minutes = access_expire_minutes
        self.refresh_expire_days = refresh_expire_days
        self._repository_refresh_token = repository_refresh_token

    async def encode(self, user: User | UserSchema, token_type: TokenEnum) -> str:
        now = datetime.datetime.utcnow()
        payload = {'sub': str(user.id), 'iat': now}
        if token_type == TokenEnum.ACCESS:
            timedelta = datetime.timedelta(minutes=self.access_expire_minutes)
            payload.update(username=user.username, email=user.email)

        elif token_type == TokenEnum.REFRESH:
            timedelta = datetime.timedelta(days=self.refresh_expire_days)

        else:
            raise ValueError('Invalid token type')

        expire = now + timedelta

        payload.update(type=token_type.value, exp=expire)
        token = jwt.encode(
            payload=payload,
            key=settings.secret_key,
            algorithm=self.algorithm
        )

        if token_type == TokenEnum.REFRESH:
            await self._repository_refresh_token.delete(sub=user.id)
            await self._repository_refresh_token.create(
                dict(sub=user.id, token=token, expires_in=expire)
            )

        return token

    async def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.secret_key,
                algorithms=[self.algorithm],
            )

        except InvalidTokenError:
            await self._repository_refresh_token.delete(token=token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid token'
            )

        return payload

    async def exists(self, sub: RefreshToken.sub | User.id) -> RefreshToken | None:
        return await self._repository_refresh_token.exists(
            sub=sub
        )

    async def logout(self, sub: RefreshToken.sub | User.id):
        await self._repository_refresh_token.delete(sub=sub)

