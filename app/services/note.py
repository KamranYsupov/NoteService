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
        
    async def create_note(create_note_tags_schema: CreateNoteSchema):
        obj_in_data = create_note_tags_schema.model_dump()
        tags_names = obj_in_data['tags_names']
        tags = self._repository_tag.bulk_create(
            tags_names=tags_names,
            returning=True,
        )
        obj_in_data['tags'] = tags
        
        return self._repository_note.create(obj_in_data)
        
        
            
            
                   
