from app.db.metods.base import update_obj
from app.db.dao.main import UserDAO, UserDB
from app.db.dao.chars import ExistenceDB, CharacterDB, CharacterDAO, ExistenceDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide

update_user = update_obj(UserDAO)
update_char = update_obj(CharacterDAO)
update_exist = update_obj(ExistenceDAO)

updade_item = update_obj(ItemDAO)

async def update_main_char(user_id: int, char_id: int) -> bool:
    return await update_user(filters={'id':user_id}, new_data={'main_char':char_id})

async def update_quantity_item(item_id: int, quantity: int) -> ItemDB:
    return await updade_item(filters={'id':item_id}, new_data={'quantity':quantity})






