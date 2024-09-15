import uuid
from typing import Dict, List

import sqlalchemy
from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.db import Note, User
from app.schemas.user import CreateUserSchema, UserSchema
from app.schemas.note import CreateNoteSchema, NoteSchema
from app.services import NoteService, UserService, TagService
from ..deps import get_current_user_access


router = APIRouter(tags=['Note'], prefix='/notes')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=NoteSchema)
@inject
async def create_note(
    create_note_schema: CreateNoteSchema,
    limit_tags: int = 20,
    user: User = Depends(get_current_user_access),
    note_service: TagService = Depends(
        Provide[Container.note_service]
    ),
    tag_service: NoteService = Depends(
        Provide[Container.tag_service]
    ),
) -> NoteSchema:
    create_note_schema.owner_id = user.id
    note = await note_service.create_note(
        obj_in=create_note_schema
    )  
    note_schema = NoteSchema(
        id=note.id,
        title=note.title,
        content=note.content,
        tags=create_note_schema.tags_names,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )
    return note_schema


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[NoteSchema])
@inject
async def get_user_notes(
    user: User = Depends(get_current_user_access),
    limit: int = 10, 
    skip: int = 0, 
    note_service: NoteService = Depends(
        Provide[Container.note_service]
    ),
) -> List[NoteSchema]:
    notes = await note_service.get_user_notes(
        owner_id=user.id,
        limit=limit,
        skip=skip
    )
    notes_schemas = [
        NoteSchema(
            id=note.id,
            title=note.title,
            content=note.content,
            tags=[tag.name for tag in note.tags],
            created_at=note.created_at,
            updated_at=note.updated_at,
        ) for note in notes
    ]
    return notes_schemas


@router.get('/by_tag_name', status_code=status.HTTP_200_OK, response_model=List[NoteSchema])
@inject
async def get_user_notes_by_tag_name(
    tag_name: str,
    user: User = Depends(get_current_user_access),
    note_service: NoteService = Depends(
        Provide[Container.note_service]
    ),
) -> List[NoteSchema]:
    notes = await note_service.get_user_notes_by_tag_name(
        owner_id=user.id,
        tag_name=tag_name
    )
    notes_schemas = [
        NoteSchema(
            id=note.id,
            title=note.title,
            content=note.content,
            tags=[tag.name for tag in note.tags],
            created_at=note.created_at,
            updated_at=note.updated_at,
        ) for note in notes
    ]
    return notes_schemas


@router.delete('/{note_id}', status_code=status.HTTP_200_OK)
@inject
async def delete_note(
    note_id: str,
    user: User = Depends(get_current_user_access),
    note_service: NoteService = Depends(
        Provide[Container.note_service]
    ),
) -> dict:
    note = await note_service.get(
        id=uuid.UUID(note_id)
    )
    if note.owner_id != user.id:
        raise HTTPException(
            detail='Вы не можете удалять чужие записи',
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        
    await note_service.delete(id=note.id)
    
    return {'message': 'Запись успешно удалена'}