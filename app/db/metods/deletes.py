from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB
from app.db.dao.chars import CharacterDAO, CharacterDB
from app.db.dao.transfer import TransferDAO
from app.db.metods.base import delete_obj, delete_objs

delete_char = delete_obj(CharacterDAO)
delete_chars = delete_objs(CharacterDAO)
delete_item = delete_obj(ItemDAO)
delete_items = delete_objs(ItemDAO)
delete_item_sketch = delete_obj(ItemSketchDAO)

async def delete_item_for_id(item_id: int):
    return await delete_item(id=item_id)

async def delete_items(item_ids: list[int]):
    return [await delete_item_for_id(item_id) for item_id in item_ids]

async def delete_items_for_sketch_id(sketch_id: int):
    return await delete_items(sketch_id=sketch_id)

async def delete_item_sketch_for_id(item_id: int):
    return await delete_item_sketch(id=item_id)

delete_transfer = delete_obj(TransferDAO)

async def delete_transfer_for_id(transfer_id: int):
    return await delete_transfer(id=transfer_id)
