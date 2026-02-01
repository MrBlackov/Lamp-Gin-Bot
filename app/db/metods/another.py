from app.db.base import Base
from app.db.connection import connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.logged.botlog import log
from pydantic import BaseModel
from app.db.dao.base import BaseDAO
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload
from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB, ExistenceDB, InventoryDB

@connection()
@log.decor()
async def get_items_and_chars_for_sketch(session: AsyncSession, sketch_id: int):
    query = (
        select(ItemSketchDB)
        .options(
            selectinload(ItemSketchDB.items).selectinload(ItemDB.inventory)
            .selectinload(InventoryDB.exist)  # Если связь есть
            .selectinload(ExistenceDB.char)   # Если связь есть
        )
        .where(ItemSketchDB.id == sketch_id)
    )
    
    result = await session.execute(query)
    sketch = result.scalar_one_or_none()
    return sketch
    
    
