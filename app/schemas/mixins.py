from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserSchemaMixin(BaseModel):
    telegram_id: Optional[int] = Field(title='Telegram ID', default=None)
    username: str = Field(title='Имя пользователя', max_length=50, min_length=8)
    email: EmailStr = Field(title='E-mail')
    
  
class NoteSchemaMixin(BaseModel):
    title: str
    content: str
      
      
class TagSchemaMixin(BaseModel):
    name: str
    
    
