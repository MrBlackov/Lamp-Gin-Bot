from aiogram.filters.callback_data import CallbackData
from typing import Any, Literal

class ItemTransferStartCall(CallbackData, prefix='item_transfer_start'):
    to_search: bool = False
    to_list: bool = False

class ItemTransferCharIdCall(CallbackData, prefix='item_transfer_char_id'):
    char_id: int
