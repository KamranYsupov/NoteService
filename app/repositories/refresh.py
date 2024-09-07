from .base import RepositoryBase
from app.db import RefreshToken


class RepositoryRefreshToken(RepositoryBase[RefreshToken]):
    """Репозиторий для работы с refresh токенами"""
