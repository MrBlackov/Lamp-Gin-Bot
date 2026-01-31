from aiogram.filters.callback_data import CallbackData
from typing import Any

class AddItemTypeCall(CallbackData, prefix='add_item_type'):
    type: str

class AddItemBackCall(CallbackData, prefix='add_item_back'):
    where: str

class AddItemMisskCall(CallbackData, prefix='add_item_Miss'):
    where: str

class AddItemToCreate(CallbackData, prefix='add_item_to_create'):
    to_create: bool = True




class ListItemSketchToPageCall(CallbackData, prefix='list_item_sketch_to_page'):
    page: int
    
class ListItemSketchItemCall(CallbackData, prefix='list_item_sketch_item'):
    item: int

class ListItemSketchBackCall(CallbackData, prefix='list_item_sketch_back'):
    where: str

class ListItemSketchToQueryCall(CallbackData, prefix='list_item_sketch_to_query'):
    pass

class ListItemSketchToListCall(CallbackData, prefix='list_item_sketch_to_list'):
    pass


class ChangeItemSketchBackCall(CallbackData, prefix='change_item_sketch_back'):
    where: str

class ChangeItemSketchCall(CallbackData, prefix='change_item_sketch'):
    is_name: bool = False 
    is_size: bool = False 
    is_desc: bool = False 
    is_image: bool = False
    is_emodzi: bool = False

class ChangeItemSketchDeleteSketchCall(CallbackData, prefix='change_item_sketch_delete_sketch'):
    is_delete: bool = False

class ChangeItemSketchDeleteItemsCall(CallbackData, prefix='change_item_sketch_delete_items'):
    is_delete: bool = False



