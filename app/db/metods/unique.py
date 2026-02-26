from app.db.base import Base
from app.db.connection import connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.logged.botlog import log
from app.db.models.transfer import TransferDB
from app.db.models.item import CraftDB, ItemDB
from sqlalchemy import select, or_

@connection(commit=False)
@log.decor()
async def get_transfers_for_item_id(
                             session: AsyncSession,
                             char_id: int,
                             item_id: int,                             
                            ):
        try:
            query = select(TransferDB).where(or_(TransferDB.buyer_items.op('@>')([item_id]), TransferDB.seller_items.op('@>')([item_id])), or_(TransferDB.buyer_id == char_id, TransferDB.seller_id == char_id))
            result = await session.execute(query)
            log.trace(query)
            record = result.scalars().all()
            log.debug(f"Select data in {TransferDB.__tablename__}, char_id: {char_id}, item_id: {item_id}, data:{[r.__dict__ for r in record]}")
            return record
        except SQLAlchemyError as e:
            log.error(e)
            raise

@connection(commit=False)
@log.decor()
async def get_crafts_for_item_id(
                             session: AsyncSession,
                             item_id: int,
                             is_ingredient: bool | None = None,
                             is_result: bool | None = None,
                             is_tool: bool | None = None,                          
                            ):
        try:
            if is_ingredient:
                query = select(CraftDB).where(CraftDB.ingredient_ids.op('@>')([item_id]))
            elif is_result:
                query = select(CraftDB).where(CraftDB.result_ids.op('@>')([item_id]))
            elif is_tool:
                query = select(CraftDB).where(CraftDB.tool_ids.op('@>')([item_id]))
            else:
                query = select(CraftDB).where(or_(CraftDB.ingredient_ids.op('@>')([item_id]), CraftDB.result_ids.op('@>')([item_id]), CraftDB.tool_ids   .op('@>')([item_id])))
            result = await session.execute(query)
            log.trace(query)
            record = result.scalars().all()
            log.debug(f"Select data in {CraftDB.__tablename__}, item_id: {item_id}, data:{[r.__dict__ for r in record]}")
            return record
        except SQLAlchemyError as e:
            log.error(e)
            raise        

