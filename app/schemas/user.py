import uuid
from typing import List
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.schemas.mixins import UserSchemaMixin
from .note import NoteSchema


class UserSchema(UserSchemaMixin):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    notes: List[NoteSchema] = []
    created_at: datetime
    updated_at: datetime
    

class CreateUserSchema(UserSchemaMixin):
    password: str = Field(title='Пароль', min_length=8)




