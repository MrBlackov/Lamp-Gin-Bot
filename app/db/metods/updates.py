from app.db.metods.base import update_obj, update_obj_for_ids, update_objs, update_obj_db
from app.db.dao.main import UserDAO, UserDB, ChatDAO, ChatDB, ChatSettingDAO, ChatSettingDB, MessageDAO, MessageDB, DonateDAO, DonateDB, UserSettingDB, UserSettingDAO
from app.db.dao.chars import ExistenceDB, CharacterDB, CharacterDAO, ExistenceDAO, CharSettingDAO, CharSettingDB
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, CraftDAO, CraftDB, SkillDAO, SkillDB, SkillSketchDAO, SkillSketchDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.dao.transfer import TransferDAO
from app.db.dao.action import ActionStateDB, ActionStateDAO
from typing import Literal
from datetime import datetime

update_user = update_obj(UserDAO)
update_user_setting = update_obj(UserSettingDAO)
update_char = update_obj(CharacterDAO)
update_char_setting = update_obj(CharSettingDAO)
update_exist = update_obj(ExistenceDAO)
update_chat = update_obj(ChatDAO)
update_donate = update_obj(DonateDAO)
update_chat_setting = update_obj(ChatSettingDAO)
update_message = update_obj(MessageDAO)

async def update_user_for_id(user_id: int, new_data: dict) -> UserDB:
    return await update_user(filters={'id':user_id}, new_data=new_data)

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

async def update_chat_setting_by_chat_id(chat_id: int, new_data: dict) -> ChatSettingDB:
    return await update_chat_setting(filters={'chat_id':chat_id}, new_data=new_data)

async def update_main_char(user_id: int, char_id: int | None = None) -> UserDB:
    return await update_user(filters={'id':user_id}, new_data={'main_char':char_id})

async def update_char_die(exist_id: int, is_die: bool = True) -> ExistenceDB:
    return await update_exist(filters={'id':exist_id}, new_data={'die':is_die})

async def update_exist_for_id(exist_id: int, new_data: dict) -> ExistenceDB:
    return await update_exist(filters={'id':exist_id}, new_data=new_data)

async def update_char_location_default(char_id: int) -> CharacterDB:
    return await update_char(filters={'id':char_id}, new_data={'location_id':1})

async def update_donat_for_id(donate_id: int, new_data: dict) -> DonateDB:
    return await update_donate(filters={'id':donate_id}, new_data=new_data)

async def update_donate_delete_char_quan(donate_id: int, new_quan: int | None = None, use_delete: int = 1):
    return await update_donat_for_id(donate_id, new_data={'delete_char_quantiry': ((new_quan - use_delete) if type(new_quan) == int else 0)})

update_item = update_obj(ItemDAO)
update_items = update_objs(ItemDAO)
update_item_for_ids = update_obj_for_ids(ItemDAO)
update_item_sketch = update_obj(ItemSketchDAO)

async def update_quantity_item(item_id: int, quantity: int) -> ItemDB:
    return await update_item(filters={'id':item_id}, new_data={'quantity':quantity})

async def update_item_for_id(item_id: int, new_data: dict) -> ItemDB:
    return await update_item(filters={'id':item_id}, new_data=new_data)

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

update_skill = update_obj(SkillDAO)
update_skill_db = update_obj_db(SkillDAO)
update_skill_sketch = update_obj(SkillSketchDAO)

async def update_skill_sketch_for_tag(tag: str, new_data: dict) -> SkillSketchDB:
    return await update_skill_sketch(filters={'tag':tag}, new_data=new_data)

async def update_skill_for_id(id: int, new_data: dict) -> SkillDB:
    return await update_skill(filters={'id':id}, new_data=new_data)

async def update_skill_for_tag(tag: str, attribute_point_id: int, new_data: dict) -> SkillDB:
    return await update_skill(filters={'sketch_tag':tag, 'attribute_point_id':attribute_point_id}, new_data=new_data)

async def update_skill_coins_for_id(id: int, new_coins: float) -> SkillDB:
    return await update_skill_for_id(id=id, new_data={'coins':new_coins})

update_action_state = update_obj(ActionStateDAO)

async def update_action_state_for_id(id: int, new_data: dict) -> ActionStateDB:
    return await update_action_state(filters={'id':id}, new_data=new_data)

async def update_action_state_for_tag(tag: str, new_data: dict) -> ActionStateDB:
    return await update_action_state(filters={'tag':tag}, new_data=new_data)









