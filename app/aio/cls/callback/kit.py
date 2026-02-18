from aiogram.filters.callback_data import CallbackData
from typing import Literal

class KitIdCall(CallbackData, prefix='kit_id'):
    kit_id: int
    is_new: bool = False

class KitBackCall(CallbackData, prefix='kit_back'):
    where: str

class KitActionCall(CallbackData, prefix='kit_action'):
    kit_id: int | None = None
    to_enter_code: bool = False
    to_get_kit: bool = False
    to_arhiv: bool = False
    to_save: bool = False

