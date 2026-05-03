from app.db.metods.base import add_or_update_obj, select_objs_for_data, select_obj, select_objs, select_objs_no_valide, select_obj_no_valide, get_for_ids
from app.db.dao.main import UserDAO, UserDB, TgUserDAO, TgUserDB, DonateDAO, DonateDB, ChatDAO, ChatSettingDAO, ChatDB, ChatSettingDB, MessageDAO, MessageDB
from app.db.dao.chars import CharacterDAO, CharacterDB, ExistenceDAO, ExistenceDB
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, KitDAO, KitDB, KitSketchDAO, KitSketchDB, CraftDB, CraftDAO, SkillDAO, SkillDB, SkillSketchDAO, SkillSketchDB
from app.validate.add.characters import Character_add, Existence_add
from app.validate.add.base import Users_add
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.dao.transfer import TransferDAO, TransferDB
from app.db.dao.action import ActionStateDAO, ActionStateDB
from app.logic.cls import MyTransfers, Craft
from datetime import datetime

add_or_update_user = add_or_update_obj(UserDAO)
add_or_update_donate = add_or_update_obj(DonateDAO)

select_user = select_obj(Users_add, UserDAO)
select_users = select_objs(Users_add, UserDAO)

select_chat = select_obj_no_valide(ChatDAO)
select_chat_setting = select_obj_no_valide(ChatSettingDAO)
select_message = select_obj_no_valide(MessageDAO)

async def get_user_for_tg_id(tg_id: int, to_user: bool = False) -> int | UserDB:
    user = await add_or_update_user(data={'tg_id':tg_id}, tg_id=tg_id)
    donate = await add_or_update_donate(data={'user_id':user.id}, user_id=user.id)
    return user if to_user else user.id 

async def get_user_for_id(user_id: int) -> UserDB:
    return await select_user(filters={'id':user_id})

async def get_users() -> list[UserDB]:
    return await select_users()

async def get_chat_for_tg_id(tg_id: int) -> ChatDB | None:
    chat: ChatDB = await select_chat(filters={'tg_id':tg_id}, logger=False)
    if chat and chat.setting_id:
        setting = await select_chat_setting(filters={'chat_id':chat.id}, logger=False)
        return chat.add_setting(setting)
    return chat

async def get_chat_setting_for_id(setting_id: int) -> ChatSettingDB | None:
    return await select_chat_setting(filters={'id':setting_id})

async def get_chat_for_id(chat_id: int) -> ChatDB | None:
    chat: ChatDB = await select_chat(filters={'id':chat_id})
    if chat and chat.setting_id:    
        setting = await select_chat_setting(filters={'chat_id':chat.id})
        return chat.add_setting(setting)
    return chat

async def get_message(tg_chat_id: int, message_id: int):
    return await select_message(filters={'chat_tg_id':tg_chat_id, 'msg_id':message_id})

select_char = select_obj(Character_add, CharacterDAO)
select_chars = select_objs(Character_add, CharacterDAO)
select_exist = select_obj(Existence_add, ExistenceDAO)

async def get_main_char_for_user_id(user_id: int) -> int | None:
    user: UserDB = await get_user_for_id(user_id)
    if user.main_char:
        return user.main_char

async def get_char_for_id(char_id: int) -> CharacterDB:
    return await select_char(filters={'id':char_id})

async def get_chars_for_user_id(user_id: int, is_die: bool | None = False) -> list[CharacterDB]:
    chars = await select_chars(filters={"user_id":user_id})
    return [c for c in chars if c.exist.die == is_die] if type(is_die) == bool else chars

async def get_all_chars() -> list[CharacterDB]:
    return await select_chars()

select_exist = select_obj_no_valide(ExistenceDAO)
select_exists_for_ids = get_for_ids(ExistenceDAO)
select_exists = select_objs_for_data(ExistenceDAO)

async def get_exist_for_id(id: int) -> ExistenceDB:
    return await select_exist(filters={'id':id})

async def get_exists_for_ids(ids: list[int]) -> list[ExistenceDB]:
    return await select_exists_for_ids(ids=ids)

select_item = select_obj(ItemValide, ItemDAO)
select_items = select_objs(ItemValide, ItemDAO)
select_item_sketch = select_obj(ItemSketchValide, ItemSketchDAO)
select_item_sketchs = select_objs(ItemSketchValide, ItemSketchDAO)
select_items_for_ids = get_for_ids(ItemDAO)

async def get_item(sketch_id: int, inventory_id: int) -> ItemDB:
    return await select_item(filters={'sketch_id':sketch_id, 'inventory_id':inventory_id})

async def get_item_sketch(sketch_id: int) -> ItemSketchDB:
    return await select_item_sketch(filters={'id':sketch_id})

async def get_item_for_id(item_id: int) -> ItemDB:
    return await select_item(filters={'id':item_id})

async def get_item_for_name(name: str) -> ItemDB:
    return await select_item_sketch(filters={'name':name})

async def get_items() -> list[ItemDB]:
    return await select_items()

async def get_items_for_inventory(inventory_id: int) -> list[ItemDB]:
    result = await select_items(filters={'inventory_id':inventory_id})
    return [r for r in result if r.is_pick_up == None] if result else []

async def get_items_for_location(location_id: int) -> tuple[list[ItemDB], list[ItemDB]]:
    result: list[ItemDB] = await select_items(filters={'location_id':location_id})
    return ([r for r in result if r.is_pick_up == False], [r for r in result if r.is_pick_up]) if result else ([], [])

async def get_items_for_ids(ids: list[int]) -> list[ItemDB] | None:
    return await select_items_for_ids(ids=ids)

async def get_item_sketchs(is_hide: bool = False) -> list[ItemSketchDB]:
    return await select_item_sketchs(filters={'is_hide':is_hide})

async def get_item_sketch_for_tag(tag: str) -> ItemSketchDB:
    return await select_item_sketch(filters={'tag':tag})

select_transfer = select_obj_no_valide(TransferDAO)
select_transfers = select_objs_no_valide(TransferDAO)

async def get_items_for_transfer(transfer_id: int, from_char: bool) -> list[ItemDB] | None:
    transfers: list[ItemDB] =  await select_items(filters={'transfer_id':transfer_id})
    transfers = [t for t in transfers if t.from_char_transfers == from_char] if transfers else []
    return transfers if len(transfers) > 0 else None

async def get_items_for_craft(craft_id: int) -> list[ItemDB] | None:
    return await select_items(filters={'craft_id':craft_id})

async def get_transfer_for_id(transfer_id: int) -> TransferDB | None:
    return await select_transfer(filters={'id':transfer_id})

async def get_transfers(char_id: int) -> MyTransfers:
    from_me = await select_transfers(filters={'seller_id':char_id})
    to_me = await select_transfers(filters={'buyer_id':char_id})
    return MyTransfers(from_me, to_me)

async def get_all_transfers() -> list[TransferDB] | None:
    return await select_transfers()


async def get_transfers_for_char_id(my_char_id: int, char_id: int) -> MyTransfers:
    from_me = await select_transfers(filters={'seller_id':my_char_id, 'buyer_id':char_id})
    to_me = await select_transfers(filters={'seller_id':char_id, 'buyer_id':my_char_id})
    return MyTransfers(from_me, to_me)

select_kit = select_obj_no_valide(KitDAO)
select_kits = select_objs_no_valide(KitDAO)
select_kit_sketch = select_objs_no_valide(KitSketchDAO)
select_kit_sketchs = select_objs_no_valide(KitSketchDAO)

async def get_kit_for_id(kit_id: int) -> KitDB | None:
    return await select_kit(filters={'id':kit_id})

async def get_kit_for_sketch_id(sketch_id: int) -> KitDB | None:
    return await select_kit(filters={'sketch_id':sketch_id})

async def get_kits(inventory_id: int | None) -> list[KitDB] | None:
    filters = {'sketch_id':inventory_id} if inventory_id else {}
    return await select_kits(filters=filters)

async def get_kit_sketch_for_id(sketch_id: int) -> KitSketchDB | None:
    return await select_kit_sketch(filters={'id':sketch_id})

async def get_kit_sketch_for_code(code: str) -> KitSketchDB | None:
    return await select_kit_sketch(filters={'code':code})

async def get_kit_sketch_for_hide(hide: bool) -> list[KitSketchDB] | None:
    return await select_kit_sketchs(filters={'hide':hide})


select_craft = select_obj_no_valide(CraftDAO)
select_crafts = select_objs_no_valide(CraftDAO)

async def get_craft_for_id(craft_id: int):
    craft: CraftDB = await select_craft(filters={'id':craft_id})
    items = await get_items_for_craft(craft.id)
    return craft.add_items(items)

async def get_crafts(is_hide: bool | None = True) -> list[CraftDB] | None:
    crafts: list[CraftDB] = await select_crafts(filters={'is_hide':is_hide, 'is_create':True}) if type(is_hide) == bool else await select_crafts()
    if crafts:
        return [craft.add_items(await get_items_for_craft(craft.id)) for craft in crafts]
    return crafts

select_skill = select_obj_no_valide(SkillDAO)
select_skills = select_objs_no_valide(SkillDAO)

select_skill_sketch = select_obj_no_valide(SkillSketchDAO)
select_skill_sketchs = select_objs_no_valide(SkillSketchDAO)

async def get_skill_for_id(id: int) -> SkillDB:
    return await select_skill(filters={'id':id})

async def get_skills_for_attribute_point_id(ap_id: int, **kwargs) -> list[SkillDB]:
    filters = {'attribute_point_id':ap_id}
    filters.update(kwargs)
    return await select_skills(filters=filters)

async def get_all_skills() -> list[SkillSketchDB]:
    return await select_skill_sketchs()

async def get_base_skills() -> list[SkillSketchDB]:
    return await select_skill_sketchs(filters={'is_base':True})

async def get_skill_for_sketch_id(sketch_id: int) -> SkillDB:
    return await select_skill(filters={'sketch_id':sketch_id})

async def get_skill_sketch_for_id(sketch_id: int) -> SkillSketchDB:
    return await select_skill_sketch(filters={'id':sketch_id})

async def get_skill_sketch_for_tag(tag: str) -> SkillSketchDB:
    return await select_skill_sketch(filters={'tag':tag})

select_action_state = select_obj_no_valide(ActionStateDAO)
select_action_states = select_objs_no_valide(ActionStateDAO)

async def get_action_state_for_id(id: int) -> ActionStateDB:
    return await select_action_state(filters={'id':id})

async def get_action_state_for_tag(tag: str, exist_id: int | None = None) -> ActionStateDB:
    filters = {'tag':tag}
    if exist_id != None:
        filters['exist_id'] = exist_id
    return await select_action_state(filters=filters)

async def get_action_states_for_exist_id(exist_id: int) -> list[ActionStateDB]:
    return await select_action_states(filters={'exist_id':exist_id})

async def get_action_states() -> list[ActionStateDB]:
    return await select_action_states()

async def get_action_states_for_block_freedom(is_block_freedom: bool, exist_id: int | None = None) -> list[ActionStateDB]:
    filters = {'is_block_freedom':is_block_freedom}
    if exist_id != None:
        filters['exist_id'] = exist_id
    return await select_action_states(filters=filters)

    