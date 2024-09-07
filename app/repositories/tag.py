from typing import List

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from app.db import Tag


class RepositoryTag(RepositoryBase[Tag]):
    """Репозиторий для работы с таблицей tags"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
        super().__init__(
            model=Tag,
            session=session,
        )
    
    async def bulk_create(
        tags_names: List[str],
        returning: bool = False,
    ) -> List[Tag] | None:
        tags_names = [tag_data['name'] for tag_data in tags_data]
        exsting_tags = self._session.query(Tag) \
            .filter(Tag.name.in_(tag_names)).all()
            
        not_existing_tags_data = [
            {'name', tag.name} for tag in exsting_tags
            if tag.name not in tags_names 
        ]
      
        statement = insert(Tag)
        
        if returning:
            statement = statement.returning(Tag)
            
        result = await self._session.execute(
            statement, not_existing_tags_data
        )
        
        return result.scalars().all()