from typing import List, Tuple

from app.db import User
from app.utils.hashers import hash_password
from .mixins import CRUDServiceMixin
from .telegram import TelegramBotService
from app.repositories.user import RepositoryUser


class UserService(CRUDServiceMixin):
    def __init__(
        self,
        repository_user: RepositoryUser,
        telegram_service: TelegramBotService,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_user = repository_user
        self.telegram_service = telegram_service
        super().__init__(
            repository=repository_user,
            unique_fields=unique_fields,
        )

    async def create_user(self, obj_in):
        obj_in_data = dict(obj_in)
        telegram_id = obj_in_data.get('telegram_id')
        
        if telegram_id:
            self.telegram_service.get_user(telegram_id) 
             
        hashed_password = hash_password(obj_in_data['password'])
        obj_in_data['password'] = hashed_password

        return await super().create(
            obj_in=obj_in_data,
        )
        
