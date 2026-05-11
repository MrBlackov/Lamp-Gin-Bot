from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class NewItemACtionCall(BaseCall, prefix='new_item_action'):
    to_argree_rules: bool = False
    to_read_rules: bool = False
    to_redact: bool = False
    redact_key: str | None = None
    to_send: bool = False
    to_create: bool = False
    to_faq: bool = False
    to_nbt: bool = False
    to_delete_nbt: bool = False 
    delete_nbt: bool = False 
    to_add_action: bool = False 
    to_action_tags: bool = False

class NewItemAdminACtionCall(BaseCall, prefix='new_item_admin_action'):
    sketch_id: int
    to_redact: bool = False
    to_create: bool | None = None    
    redact_item: bool = False

class NewItemBackCall(BaseCall, prefix='new_item_back'):
    where: str

class NewItemSketchDeleteActionTagCall(BaseCall, prefix='new_item_sketch_delete_action_tag'):
    tag: str
    is_delete: bool = False





class ListItemSketchToPageCall(BaseCall, prefix='list_item_sketch_to_page'):
    page: int
    
class ListItemSketchItemCall(BaseCall, prefix='list_item_sketch_item'):
    item: int

class ListItemSketchBackCall(BaseCall, prefix='list_item_sketch_back'):
    where: str

class ListItemSketchToQueryCall(BaseCall, prefix='list_item_sketch_to_query'):
    pass

class ListItemSketchToListCall(BaseCall, prefix='list_item_sketch_to_list'):
    is_hide: bool = False 



class GiveItemBackCall(BaseCall, prefix='give_item_back'):
    where: str
class GiveItemCall(BaseCall, prefix='give_item'):
    sketch_id: int

class GiveItemActionCall(BaseCall, prefix='give_item_action'):
    to_quantity: bool = False
    to_change_char: bool = False
    to_give: bool = False


class ChangeItemSketchIDCall(BaseCall, prefix='change_item_sketch_id'):
    sketch_id: int

class ChangeItemSketchBackCall(BaseCall, prefix='change_item_sketch_back'):
    where: str

class ChangeItemSketchToPageCall(BaseCall, prefix='change_item_sketch_to_page'):
    page: int

class ChangeItemSketchItemCall(BaseCall, prefix='change_item_sketch_item'):
    item_id: int

class ChangeItemSketchCall(BaseCall, prefix='change_item_sketch'):
    what: str | None = None
    to_items: bool = False
    to_nbt: bool = False
    to_delete_nbt: bool = False

class ChangeItemSketchDeleteActionTagCall(BaseCall, prefix='change_item_sketch_delete_action_tag'):
    tag: str
    is_delete: bool = False

class ChangeItemSketchAddActionTagCall(BaseCall, prefix='change_item_sketch_add_action_tag'):
    pass

class ChangeItemSketchDeleteSketchCall(BaseCall, prefix='change_item_sketch_delete_sketch'):
    is_delete: bool = False

class ChangeItemSketchDeleteItemsCall(BaseCall, prefix='change_item_sketch_delete_items'):
    is_delete: bool = False

class ChangetemSketchItemInCharCall(BaseCall, prefix='change_item_sketch_item_in_inventory'):
    item_id: int
    action: Literal['+', '-'] = '-'



