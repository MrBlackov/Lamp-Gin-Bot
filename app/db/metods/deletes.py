from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB
from app.db.metods.base import delete_obj

delete_item = delete_obj(ItemDAO)

async def delete_item_for_id(item_id: int):
    return await delete_item(id=item_id)

