from app.db.metods.base import add_or_update_obj, add_obj, add_obj_dict, add_db_obj, update_obj
from app.db.dao.main import TgChatDAO, TgUserDAO, DonateDAO, ChatDAO, TgChatDB, ChatSettingDAO, ChatDB, ChatSettingDB, MessageDAO, MessageDB
from app.db.dao.chars import CharacterDAO, ExistenceDAO, AttributePointDAO, InventoryDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, KitSketchDB, KitDB, KitDAO, KitSketchDAO
from app.db.dao.transfer import TransferDAO, TransferDB
from aiogram.types import TelegramObject, User, Chat
from datetime import datetime

add_or_update_tg_user = add_or_update_obj(TgUserDAO)
add_or_update_tg_chat = add_or_update_obj(TgChatDAO)
add_or_update_chat = add_or_update_obj(ChatDAO)
add_or_update_chat_setting = add_or_update_obj(ChatSettingDAO)
add_chat_setting = add_obj_dict(ChatSettingDAO)
add_or_update_message = add_or_update_obj(MessageDAO)
add_message = add_obj_dict(MessageDAO)

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
    await update_obj(ChatDAO)(filters={'id':chat.id}, new_data={'setting_id':setting.id})
    return chat.add_setting(setting)
    
async def add_message_delete(chat_id: int, message_id: int, time_delete: datetime, is_delete: bool = True) -> MessageDB:
    return await add_message(data={'chat_tg_id':chat_id, 'msg_id':message_id, 'time_delete':time_delete, 'is_delete':is_delete})

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

