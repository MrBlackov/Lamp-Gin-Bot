from app.aio.cls.callback.base import BaseCall
from typing import Literal

class AddCharGenderCall(BaseCall, prefix='add_char_gender'):
    gender: Literal['M', 'W']
    to_change: bool = False

class AddCharNameCall(BaseCall, prefix='add_char_name'):
    regim: Literal['query', 'random'] | None = None
    first_name: bool = True
    back: bool = False
    to_pass: bool = False
    get_bonus: bool = False

class AddCharRandomNameCall(BaseCall, prefix='add_char_name_random'):
    name: str | None = None
    regeneration: bool = False
    back: bool = False
    first_name: bool = True

class AddCharQueryNameCall(BaseCall, prefix='add_char_name_query'):
    name: str | None = None
    page: int = 0
    next_page: bool = False
    first_name: bool = True
    back: bool = False

class AddCharSketchCall(BaseCall, prefix='add_char_sketch'):
    id: int | None = None
    another: bool | None = None
    back: bool = False

class AddCharDescriptCall(BaseCall, prefix='add_char_descript'):
    to_pass: bool = False
    back: bool = False
 
class AddCharFinishCall(BaseCall, prefix='add_char_finish'):
    go: bool | None = None


class InfoCharListCall(BaseCall, prefix='info_char_list'):
    char_id: int
    main: bool = False

class InfoCharChooseCall(BaseCall, prefix='info_char_chouse'):
    char_id: int | None = None
    back: bool = False

class InfoCharDeleteCall(BaseCall, prefix='info_char_delete'):
    char_id: int | None = None
    exist_id: int | None = None
    is_delete: bool = False
    back: bool = False

class InventoryItemsCall(BaseCall, prefix='inventory_items'):
    item: int

class InventoryItemsPickUpCall(BaseCall, prefix='inventory_items'):
    item_id: int
    to_pick_up: bool = False

class InventoryItemsGoCall(BaseCall, prefix='inventory_items_go'):
    where: str
    item_id: int | None = None

class InventoryItemsActionCall(BaseCall, prefix='inventory_items_action'):
    to_throw: bool = False
    to_pick_up: bool = False
