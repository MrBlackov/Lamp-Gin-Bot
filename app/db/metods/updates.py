from app.db.metods.base import update_obj
from app.db.dao.main import UserDAO, UserDB
from app.db.dao.chars import ExistenceDB, CharacterDB, CharacterDAO, ExistenceDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.dao.transfer import TransferDAO

update_user = update_obj(UserDAO)
update_char = update_obj(CharacterDAO)
update_exist = update_obj(ExistenceDAO)


update_item = update_obj(ItemDAO)
update_item_sketch = update_obj(ItemSketchDAO)


async def update_main_char(user_id: int, char_id: int) -> bool:
    return await update_user(filters={'id':user_id}, new_data={'main_char':char_id})

async def update_quantity_item(item_id: int, quantity: int) -> ItemDB:
    return await update_item(filters={'id':item_id}, new_data={'quantity':quantity})

async def update_quantity_items(items: dict[int, int]) -> list[ItemDB]:
    return [await update_quantity_item(item_id, quantity) for item_id, quantity in items.items()]

async def update_item_sketch_for_id(item_id: int, new_data: dict) -> ItemSketchDB:
    return await update_item_sketch(filters={'id':item_id}, new_data=new_data)

update_transfer = update_obj(TransferDAO)
