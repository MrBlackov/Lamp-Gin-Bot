from app.db.base import Base
from app.db.connection import connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.logged.botlog import log
from pydantic import BaseModel
from app.db.dao.base import BaseDAO

def add_obj(clsDAO: BaseDAO):
    @connection()
    @log.decor()
    async def add_new_obj(
                          session: AsyncSession,
                          data: BaseModel,
                          logger: bool = True
                         ):
        new_data = await clsDAO.add(session, data)
        if logger: log.info(f"New data in {new_data.__tablename__}, id: {new_data.id}, data:{data.model_dump()}")
        else: log.trace(f"New data in {new_data.__tablename__}, id: {new_data.id}, data:{data.model_dump()}")
        return new_data

    return add_new_obj

@connection()
@log.decor(arg=True)
async def add_db_obj(
                      session: AsyncSession,
                      data: list[Base] | None,
                      logger: bool = True
                     ):
    if data == None or len(data) == 0:
        return None
    try:
        session.add_all(data)
        await session.flush()
        if logger: log.info(f"New data in {[d.__tablename__ for d in data]}, data:{[d.__dict__ for d in data]}")
        else: log.trace(f"New data in {[d.__tablename__ for d in data]}, data: {[d.__dict__ for d in data]}")
        return data
    except SQLAlchemyError as e:
        await session.rollback()
        raise e



def add_obj_dict(clsDAO: BaseDAO):
    @connection()
    @log.decor()
    async def add_new_obj(
                          session: AsyncSession,
                          data: dict,
                          logger: bool = True
                         ):
        new_data = await clsDAO.add_dict(session, data)
        if logger: log.info(f"New data in {new_data.__tablename__}, id: {new_data.id}, data:{data}")
        else: log.trace(f"New data in {new_data.__tablename__}, id: {new_data.id}, data:{data}")
        return new_data

    return add_new_obj

def add_or_update_obj(clsDAO: BaseDAO):
    @connection()
    @log.decor()
    async def add_new_obj(
                          session: AsyncSession,
                          data: dict,
                          logger: bool = True,
                          **kwargs
                         ):
        new_data = await clsDAO.add_or_update(session, data, **kwargs)
        return new_data

    return add_new_obj



def select_obj(clsP: BaseModel, clsDAO: BaseDAO,):
    @connection()
    @log.decor()
    async def _select_obj(                      
                          session: AsyncSession,
                          filters: dict,
                          logger: bool = True
                        ):
        data = await clsDAO.find_one_or_none(session, filters)
        if logger and data: log.info(f"Select data in {data.__tablename__}, id: {data.id}, data:{clsP.model_validate(data).model_dump()}")
        elif data: log.trace(f"Select data in {data.__tablename__}, id: {data.id}, data:{clsP.model_validate(data).model_dump()}")
        elif logger: log.info(f"Select data in None, filtres: {filters}")
        else: log.trace(f"Select data in None, filtres: {filters}")
         
        return data 
        
    return _select_obj

def select_obj_no_valide(clsDAO: BaseDAO,):
    @connection()
    @log.decor()
    async def _select_obj(                      
                          session: AsyncSession,
                          filters: dict,
                          logger: bool = True
                        ):
        data = await clsDAO.find_one_or_none(session, filters)
        if logger and data: log.info(f"Select data in {data.__tablename__}, id: {data.id}, data:{data.__dict__}")
        elif data: log.trace(f"Select data in {data.__tablename__}, id: {data.id}, data:{data.__dict__}")
        elif logger: log.info(f"Select data in None, filtres: {filters}")
        else: log.trace(f"Select data in None, filtres: {filters}")
         
        return data 
        
    return _select_obj

def select_objs(clsP: BaseModel, clsDAO: BaseDAO,):
    @connection(commit=False)
    @log.decor()
    async def _select_objs(                      
                          session: AsyncSession,
                          filters: dict | None = None,
                          logger: bool = True
                        ):
        data = await clsDAO.find_all(session, filters)
        if logger and data: log.info(f"Select data in {data[0].__tablename__} datas:{[clsP.model_validate(d).model_dump() for d in data]}")
        elif data: log.trace(f"Select data in {data[0].__tablename__} datas:{[clsP.model_validate(d).model_dump() for d in data]}")
        elif logger: log.info(f'Select None, DAO: {clsDAO.model.__tablename__}, filtres: {filters}')
        else: log.trace(f'Select None, DAO: {clsDAO.model.__tablename__}, filtres: {filters}')               
        return data
    return _select_objs

def select_objs_no_valide(clsDAO: BaseDAO):
    @connection(commit=False)
    @log.decor()
    async def _select_objs(                      
                          session: AsyncSession,
                          filters: dict | None = None,
                          logger: bool = True
                        ):
        data = await clsDAO.find_all(session, filters)
        if logger and data: log.info(f"Select data in {data[0].__tablename__} datas:{[d.__dict__ for d in data]}")
        elif data: log.trace(f"Select data in {data[0].__tablename__} datas:{[d.__dict__ for d in data]}")
        elif logger: log.info(f'Select None, DAO: {clsDAO.model.__tablename__}, filtres: {filters} datas:{[d.__dict__ for d in data]}')
        else: log.trace(f'Select None, DAO: {clsDAO.model.__tablename__}, filtres: {filters} datas:{[d.__dict__ for d in data]}')               
        return data
    return _select_objs


def update_obj(clsDAO: BaseDAO):
    @connection()
    @log.decor()
    async def update_(session: AsyncSession, filters: dict, new_data: dict):
        data_find = await clsDAO.find_one_or_none(session, filters=filters)
        update = await clsDAO.update_one(session, record=data_find, values=new_data)
        return update
    return update_

def delete_obj(clsDAO: BaseDAO):
    @connection()
    @log.decor()
    async def delete_obj_(session: AsyncSession, id: int | None = None, logger: bool = True, **kwargs):
        try:
            if id:
                data_id = id
            elif kwargs:
                data_find = await clsDAO.find_one_or_none(session, filters=kwargs)
                data_id = data_find.id
            else:
               return False

            await clsDAO.delete_one_by_id(session=session, data_id=data_id)
            if logger:    
                log.info(f"Delete data in {clsDAO.model.__tablename__}), id: {id}, kwargs:{kwargs}")
            else:
                log.trace(f"Delete data in {clsDAO.model.__tablename__}), id: {id}, kwargs:{kwargs}")
    
            return True
        except SQLAlchemyError as sqle:
            log.warning(sqle)
            raise sqle
        

    return delete_obj_

def delete_objs(clsDAO: BaseDAO,):
    @connection()
    @log.decor()
    async def delete_obj_s(session: AsyncSession, logger: bool = True, **kwargs):
        try:
            data_find = await clsDAO.find_all(session, filters=kwargs)

            if data_find:
                await clsDAO.delete_many(session, filters=kwargs)
                return_value = True
            else: 
                return_value = False

            if logger:    
                log.info(f"Delete data(killed) in {clsDAO.model.__tablename__}, id: {id}, kwargs:{kwargs}")
            else:
                log.trace(f"Delete data(killed) in {clsDAO.model.__tablename__}, id: {id}, kwargs:{kwargs}")
    
            return return_value
        except SQLAlchemyError as sqle:
            log.warning(sqle)
            raise sqle
        
    return delete_obj_s

