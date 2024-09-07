import uuid
from typing import List, TYPE_CHECKING
from datetime import datetime

from .mixins import NoteSchemaMixin



class NoteSchema(NoteSchemaMixin):
    id: uuid.UUID
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    
class CreateNoteSchema(NoteSchemaMixin):
    owner_id: uuid.UUID
    tags_names: List[str] = []