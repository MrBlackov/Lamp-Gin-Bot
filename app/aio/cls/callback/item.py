from aiogram.filters.callback_data import CallbackData
from typing import Literal

class AddItemTypeCall(CallbackData, prefix='add_item_type'):
    type: str

class AddItemBackCall(CallbackData, prefix='add_item_back'):
    where: str

class AddItemMisskCall(CallbackData, prefix='add_item_Miss'):
    where: str

class AddItemToCreate(CallbackData, prefix='add_item_to_create'):
    to_create: bool = True