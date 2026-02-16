from app.db.base import Base
from app.db.connection import connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.logged.botlog import log
from app.db.models.transfer import TransferDB
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



