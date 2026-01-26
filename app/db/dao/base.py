from typing import List, Generic, TypeVar, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel
from app.db.base import Base
from app.logged.botlog import log

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: type[T] # Устанавливается в дочернем классе
    
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: dict, order = None):
        # Найти одну запись по фильтрам
        try:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: dict | None = None, order_by: dict | None = None):
        filter_dict = filters if filters else {}
        order_dict = order_by if order_by else {}        

        try:
            query = select(cls.model).filter_by(**filter_dict).order_by(**order_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        # Добавить одну запись
        try:
            values_dict = values.model_dump(exclude_unset=True)
            new_instance = cls.model(**values_dict)
            session.add(new_instance)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_dict(cls, session: AsyncSession, values: dict):
        # Добавить одну запись
        try:
            new_instance = cls.model(**values)
            session.add(new_instance)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
    
    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        # Добавить несколько записей
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances
        
    @classmethod
    async def add_or_update(cls, session: AsyncSession, data: dict, **filters) -> Base:
        try:
            select_data: Base = await cls.find_one_or_none(session, filters=filters)
            
            if select_data:
                update = await cls.update_one_by_id_no_valid(session, select_data.id, values_dict=data)
                datas = await cls.find_one_or_none(session, filters=filters)

            else:
                datas = cls.model(**data)
                session.add(datas)

            await session.flush()

            return datas
        except Exception as e:
            await session.rollback()
            raise

    @classmethod
    async def update_one_by_id_no_valid(cls, session: AsyncSession, data_id: int, values_dict: dict):
        try:
            record = await session.get(cls.model, data_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            await session.flush()
            return True
        except SQLAlchemyError as sqle:
            log.error(sqle)
            raise   
        except Exception as e:
            log.error(e)
            raise   

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: BaseModel) -> Base:
        values_dict = values.model_dump(exclude_unset=True)
        try:
            record = await session.get(cls.model, data_id)
            return await cls.update_one(record=record, values=values_dict)
        except SQLAlchemyError as e:
            log.error(e)
            raise   
  
    @classmethod
    async def update_one(cls, session: AsyncSession, record: Base, values: dict):
        try:
            for key, value in values.items():
                setattr(record, key, value)
            await session.flush()
            return record
        except SQLAlchemyError as e:
            log.error(e)
            raise          

    @classmethod
    async def update_many(cls, session: AsyncSession, filter_criteria: BaseModel, values: BaseModel):
        filter_dict = filter_criteria.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        try:
            stmt = (
                update(cls.model)
                .filter_by(**filter_dict)
                .values(**values_dict)
            )
            result = await session.execute(stmt)
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            log.error(f"Error in mass update: {e}")
            raise e
    
    @classmethod
    async def delete_one_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()
            return True
        except SQLAlchemyError as e:
            log.error(f"Error occurred: {e}")
            raise
    
    @classmethod
    async def delete_many(cls, session: AsyncSession, filters: dict | None = None):
        if filters:
            stmt = delete(cls.model).filter_by(**filters)
        else:
            stmt = delete(cls.model)
        try:
            result = await session.execute(stmt)
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            log.error(f"Error occurred: {e}")
            raise
