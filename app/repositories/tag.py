from typing import List

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import RepositoryBase
from app.db import Tag


class RepositoryTag(RepositoryBase[Tag]):
    """Репозиторий для работы с таблицей tags"""
    
    def __init__(
        self, 
        model,
        session: AsyncSession
    ):
        self._session = session
        super().__init__(
            model=model,
            session=session,
        )
    
    async def bulk_create(
        self, 
        tags_names: List[str],
        returning: bool = False,
    ) -> List[Tag] | None:
        select_statement = select(Tag).filter(Tag.name.in_(tags_names))
        select_result = await self._session.execute(select_statement)
        exsting_tags = select_result.scalars().all()
        exsting_tags_names = [tag.name for tag in exsting_tags]
            
        not_existing_tags_data = [
            {'name': tag_name} for tag_name in tags_names
            if tag_name not in exsting_tags_names  
        ]
        
        if not not_existing_tags_data:
            return exsting_tags
        
        insert_statement = insert(Tag)
        
        if returning:
            insert_statement = insert_statement.returning(Tag)
            
        insert_result = await self._session.execute(
            insert_statement, not_existing_tags_data
        )
        
        if insert_result:
            exsting_tags.extend(insert_result.scalars().all())
            return exsting_tags