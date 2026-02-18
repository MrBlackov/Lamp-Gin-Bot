from aiogram.filters.callback_data import CallbackData
from typing import Literal

class AddCharGenderCall(CallbackData, prefix='add_char_gender'):
    gender: Literal['M', 'W']
    to_change: bool = False

class AddCharNameCall(CallbackData, prefix='add_char_name'):
    regim: Literal['query', 'random'] | None = None
    first_name: bool = True
    back: bool = False
    to_pass: bool = False
    get_bonus: bool = False

class AddCharRandomNameCall(CallbackData, prefix='add_char_name_random'):
    name: str | None = None
    regeneration: bool = False
    back: bool = False
    first_name: bool = True

class AddCharQueryNameCall(CallbackData, prefix='add_char_name_query'):
    name: str | None = None
    page: int = 0
    next_page: bool = False
    first_name: bool = True
    back: bool = False

class AddCharSketchCall(CallbackData, prefix='add_char_sketch'):
    id: int | None = None
    another: bool | None = None
    back: bool = False

class AddCharDescriptCall(CallbackData, prefix='add_char_descript'):
    to_pass: bool = False
    back: bool = False
 
class AddCharFinishCall(CallbackData, prefix='add_char_finish'):
    go: bool | None = None


class InfoCharList(CallbackData, prefix='info_char_list'):
    char_id: int
    main: bool = False

class InfoCharChouse(CallbackData, prefix='info_char_chouse'):
    char_id: int | None = None
    back: bool = False


class InventoryItems(CallbackData, prefix='inventory_items'):
    item: int

class InventoryItemsGo(CallbackData, prefix='inventory_items_go'):
    where: str

class InventoryItemsThrow(CallbackData, prefix='inventory_items_throw'):
    throw: bool = True


