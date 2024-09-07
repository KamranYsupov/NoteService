from uuid import UUID
from typing import (
    Generic,
    Optional,
    Type,
    TypeVar,
    List,
    Tuple
)

from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class RepositoryBase(Generic[ModelType,]):
    """Репозиторий с базовым CRUD"""

    def __init__(
            self,
            model: Type[ModelType],
            session: AsyncSession,
    ) -> None:
        self.model = model
        self._session = session
        

    async def create(
            self, 
            insert_data: dict,
    ) -> ModelType:
        db_obj = self.model(**insert_data)

        self._session.add(db_obj)
        await self._session.flush()
        await self._session.commit()
        await self._session.refresh(db_obj)

        return db_obj

    async def get(self, **kwargs) -> Optional[ModelType]:
        statement = select(self.model).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()
    
    async def update(
            self,
            *,
            obj_id: UUID,
            insert_data: dict,
    ) -> ModelType:
        statement = (
            update(self.model).
            where(self.model.id == obj_id).
            values(**insert_data)
        )
        await self._session.execute(statement)
        await self._session.commit()

        return await self._session.get(self.model, obj_id)


    async def list(self, *args, limit: int, **kwargs):
        statement = (
            select(self.model)
            .filter(*args)
            .filter_by(**kwargs)
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def delete(self, **kwargs) -> None:
        statement = delete(self.model).filter_by(**kwargs)
        await self._session.execute(statement)

    async def exists(self, *args, **kwargs) -> Optional[ModelType]:
        statement = select(self.model).filter(or_(*args)).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()
    

