from typing import List, Tuple

from app.db import Tag
from app.utils.hashers import hash_password
from .mixins import CRUDServiceMixin
from app.repositories.tag import RepositoryTag


class TagService(CRUDServiceMixin):
    def __init__(
        self,
        repository_tag: RepositoryTag,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_tag = repository_tag
        super().__init__(
            repository=repository_tag,
            unique_fields=unique_fields,
        )
