from pydantic import BaseModel, Field


class AuthUserSchema(BaseModel):
    username: str = Field(title='Имя пользователя', max_length=50, min_length=8)
    password: str = Field(title='Пароль', min_length=8)


class TokenInfoSchema(BaseModel):
    access_token: str | None
    refresh_token: str | None = None
    token_type: str = Field(title='Тип токена', default='bearer')
