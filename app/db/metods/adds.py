from app.db.metods.base import add_or_update_obj, add_obj, add_obj_dict, add_db_obj
from app.db.dao.main import TgChatDAO, TgUserDAO, DonateDAO, ChatDAO, TgChatDB, ChatSettingDAO, ChatDB, ChatSettingDB
from app.db.dao.chars import CharacterDAO, ExistenceDAO, AttributePointDAO, InventoryDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, KitSketchDB, KitDB, KitDAO, KitSketchDAO
from app.db.dao.transfer import TransferDAO, TransferDB
from aiogram.types import TelegramObject, User, Chat

add_or_update_tg_user = add_or_update_obj(TgUserDAO)
add_or_update_tg_chat = add_or_update_obj(TgChatDAO)
add_or_update_chat = add_or_update_obj(ChatDAO)
add_or_update_chat_setting = add_or_update_obj(ChatSettingDAO)
add_chat_setting = add_obj_dict(ChatSettingDAO)

async def add_chat(chat: Chat):
    tgchat: TgChatDB = await add_or_update_tg_chat(data={'tg_id':chat.id, 
                                      'tg_type':chat.type.upper(), 
                                      'fullname':chat.full_name, 
                                      'username':chat.username, 
                                      'data':chat.__dict__}, 
                                tg_id=chat.id)
    print(tgchat.tg_id)
    chat: ChatDB =  await add_or_update_chat(data={'tg_id':chat.id},
                                    tg_id=chat.id)
    print(chat.tg_id)
    setting = await add_or_update_chat_setting(data={'chat_id':chat.id}, chat_id=chat.id)
    print(setting.id)
    return chat.add_setting(setting)
    

add_char = add_obj(CharacterDAO)
add_exist = add_obj(ExistenceDAO)
add_attribute = add_obj(AttributePointDAO)
add_inventory = add_obj(InventoryDAO)

add_char_dict = add_obj_dict(CharacterDAO)
add_exist_dict = add_obj_dict(ExistenceDAO)
add_attribute_dict = add_obj_dict(AttributePointDAO)
add_inventory_dict = add_obj_dict(InventoryDAO)

add_item = add_obj(ItemDAO)
add_item_dict = add_obj_dict(ItemDAO)
add_items_db = add_db_obj
add_item_sketch = add_obj(ItemSketchDAO)

add_kit = add_obj(KitDAO)
add_kit_dict = add_obj_dict(KitDAO)
add_kit_sketch = add_obj(KitSketchDAO)

add_transfer_dict = add_obj_dict(TransferDAO)

