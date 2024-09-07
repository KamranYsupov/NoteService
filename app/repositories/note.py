import uuid
from typing import List

from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from app.db import Note


class RepositoryNote(RepositoryBase[Note]):
    """Репозиторий для работы с таблицей notes"""
    
    def __init__(
        self, 
        model,
        session: AsyncSession,
        ):
        self._session = session
        super().__init__(
            model=model,
            session=session,
        )
        
    async def get_user_notes(
        self,
        owner_id: uuid.UUID,
        limit: int, 
        skip: int,
    ) -> List[Note]:
        statement = (
            select(Note)
            .options(selectinload(Note.tags))
            .filter_by(owner_id=owner_id)
            .limit(limit)
            .offset(skip)            
        )
        
        
        result = await self._session.execute(statement)
        
        return result.scalars().all()