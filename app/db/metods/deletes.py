from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB
from app.db.dao.chars import CharacterDAO, CharacterDB
from app.db.metods.base import delete_obj, delete_objs

delete_char = delete_obj(CharacterDAO)
delete_chars = delete_objs(CharacterDAO)
delete_item = delete_obj(ItemDAO)

async def delete_item_for_id(item_id: int):
    return await delete_item(id=item_id)