from app.db.metods.base import add_or_update_obj, add_obj, add_obj_dict, add_db_obj
from app.db.dao.main import TgChatDAO, TgUserDAO
from app.db.dao.chars import CharacterDAO, SavingDAO, ExistenceDAO, AttributePointDAO, InventoryDAO
from app.validate.add.characters import Character_add, Existence_add

add_or_update_tg_user = add_or_update_obj(TgUserDAO)
add_or_update_tg_chat = add_or_update_obj(TgChatDAO)

add_char = add_obj(CharacterDAO)
add_exist = add_obj(ExistenceDAO)
add_saving = add_obj(SavingDAO)
add_attribute = add_obj(AttributePointDAO)
add_inventory = add_obj(InventoryDAO)

add_char_dict = add_obj_dict(CharacterDAO)
add_exist_dict = add_obj_dict(ExistenceDAO)
add_saving_dict = add_obj_dict(SavingDAO)
add_attribute_dict = add_obj_dict(AttributePointDAO)
add_inventory_dict = add_obj_dict(InventoryDAO)


async def add_full_char(data: Existence_add):
    data_dict = data.model_dump()
    saving = data_dict.pop('saving', None)
    point = data_dict.pop('attibute_point', None)
    inventory = data_dict.pop('inventory', None)    
    exist = add_char_dict(data=data_dict)


async def add_full_char(data: Character_add):
    data_dict = data.model_dump()
    exist = data_dict.pop('exist')
    char = add_char_dict(data=data_dict)







