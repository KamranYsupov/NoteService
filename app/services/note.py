import uuid
from typing import List, Tuple

from app.db import Note
from app.utils.hashers import hash_password
from .mixins import CRUDServiceMixin
from app.schemas.note import CreateNoteSchema
from app.repositories import RepositoryNote, RepositoryTag


class NoteService(CRUDServiceMixin):
    def __init__(
        self,
        repository_note: RepositoryNote,
        repository_tag: RepositoryTag,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_note = repository_note
        self._repository_tag = repository_tag
        super().__init__(
            repository=repository_note,
            unique_fields=unique_fields,
        )
        
    async def create_note(self, obj_in):
        obj_in_data = dict(obj_in)
        tags_names = obj_in_data.pop('tags_names')
        print(tags_names)
        tags = await self._repository_tag.bulk_create(
            tags_names=tags_names,
            returning=True,
        )
        obj_in_data['tags'] = tags
        
        return await self._repository_note.create(obj_in_data)
    
    async def get_user_notes(
        self, 
        owner_id: uuid.UUID,
        limit: int, 
        skip: int,
    ) -> List[Note]:
        return await self._repository_note.get_user_notes(
            owner_id=owner_id,
            limit=limit,
            skip=skip
        )
        
    async def get_user_notes_by_tag_name(
        self,
        owner_id: uuid.UUID, 
        tag_name: str,
    ):
        return await self._repository_note.get_user_notes_by_tag_name(
            owner_id=owner_id,
            tag_name=tag_name
        )
        
            