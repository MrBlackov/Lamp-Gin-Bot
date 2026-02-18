from app.db.metods.base import add_or_update_obj, add_obj, add_obj_dict, add_db_obj
from app.db.dao.main import TgChatDAO, TgUserDAO
from app.db.dao.chars import CharacterDAO, ExistenceDAO, AttributePointDAO, InventoryDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB, KitSketchDB, KitDB, KitDAO, KitSketchDAO
from app.db.dao.transfer import TransferDAO, TransferDB

add_or_update_tg_user = add_or_update_obj(TgUserDAO)
add_or_update_tg_chat = add_or_update_obj(TgChatDAO)

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

