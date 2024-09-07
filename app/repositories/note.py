from .base import RepositoryBase
from app.db import Note


class RepositoryNote(RepositoryBase[Note]):
    """Репозиторий для работы с таблицей notes"""