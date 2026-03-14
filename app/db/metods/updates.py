from app.db.metods.base import update_obj, update_obj_for_ids
from app.db.dao.main import UserDAO, UserDB, ChatDAO, ChatDB, ChatSettingDAO, ChatSettingDB, MessageDAO, MessageDB
from app.db.dao.chars import ExistenceDB, CharacterDB, CharacterDAO, ExistenceDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, CraftDAO, CraftDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.dao.transfer import TransferDAO
from typing import Literal
from datetime import datetime

update_user = update_obj(UserDAO)
update_char = update_obj(CharacterDAO)
update_exist = update_obj(ExistenceDAO)
update_chat = update_obj(ChatDAO)
update_chat_setting = update_obj(ChatSettingDAO)
update_message = update_obj(MessageDAO)

async def update_chat_by_setting(chat_id: int, setting_id: int) -> ChatDB:
    return await update_chat(filters={'id':chat_id}, new_data={'setting_id':setting_id})

async def update_chat_setting_by_id(setting_id: int, msg_delete_time: int | None = None, is_msg_delete: bool | None = None) -> ChatSettingDB:
    new_data = {}
    if msg_delete_time is not None:
        new_data['msg_delete_time'] = msg_delete_time
    if is_msg_delete is not None:
        new_data['is_msg_delete'] = is_msg_delete
    print(new_data)
    print(setting_id)
    return await update_chat_setting(filters={'id':setting_id}, new_data=new_data)

async def update_chat_setting_by_chat_id(chat_id: int, msg_delete_time: int | None = None, is_msg_delete: bool | None = None) -> ChatSettingDB:
    new_data = {}
    if msg_delete_time is not None:
        new_data['msg_delete_time'] = msg_delete_time
    if is_msg_delete is not None:
        new_data['is_msg_delete'] = is_msg_delete
    print(new_data)
    return await update_chat_setting(filters={'chat_id':chat_id}, new_data=new_data)

async def update_main_char(user_id: int, char_id: int) -> bool:
    return await update_user(filters={'id':user_id}, new_data={'main_char':char_id})

async def update_char_location_default(char_id: int) -> bool:
    return await update_char(filters={'id':char_id}, new_data={'location_id':1})



update_item = update_obj(ItemDAO)
update_item_for_ids = update_obj_for_ids(ItemDAO)
update_item_sketch = update_obj(ItemSketchDAO)

async def update_quantity_item(item_id: int, quantity: int) -> ItemDB:
    return await update_item(filters={'id':item_id}, new_data={'quantity':quantity})

async def update_look_location_item(item_id: int, inventory_id: int, is_pick_up: bool) -> ItemDB:
    if is_pick_up:
        return await update_item(filters={'id':item_id}, new_data={'inventory_id':inventory_id, 'nbt': {'is_pick_up': is_pick_up}})
    return await update_item(filters={'id':item_id}, new_data={'inventory_id':None, 'nbt': {'is_pick_up': False}})
        
async def update_items_pick_up_for_ids(ids: list[int]):
    return await update_item_for_ids(ids=ids, new_data={'inventory_id':None, 'nbt': {'is_pick_up':False}})

async def update_item_throw_away(item_id: int, location_id: int) -> ItemDB:
    return await update_item(filters={'id':item_id}, new_data={'inventory_id':None, 'location_id':location_id, 'nbt': {'is_pick_up': False}})

async def update_quantity_items(items: dict[int, int]) -> list[ItemDB]:
    return [await update_quantity_item(item_id, quantity) for item_id, quantity in items.items()]

async def update_item_sketch_for_id(item_id: int, new_data: dict) -> ItemSketchDB:
    return await update_item_sketch(filters={'id':item_id}, new_data=new_data)

update_transfer = update_obj(TransferDAO)

update_craft = update_obj(CraftDAO)

async def update_craft_items(craft_id: int, new_data: list[int], type: Literal['ingredient', 'tool', 'result']) -> CraftDB:
    return await update_craft(filters={'id':craft_id}, new_data={f'{type}_ids': new_data})

async def update_item_on_craft_id(craft_id: int, item_ids: list[int]):
    return await update_item_for_ids(ids=item_ids, new_data={'craft_id':craft_id})

async def update_craft_to_create(craft_id: int) -> CraftDB:
    return await update_craft(filters={'id':craft_id}, new_data={'is_create':True})

