from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from room_reservation.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> ModelType | None:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )

        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        session: AsyncSession,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        session: AsyncSession,
        db_obj: ModelType,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
