from aiogram.filters.callback_data import CallbackData
from typing import Any, Literal
from app.enum_type.transfer import ItemTransferStatusEnum

class ItemTransferStartCall(CallbackData, prefix='item_transfer_start'):
    to_trade: bool = False

class ItemTransferChoiseCharCall(CallbackData, prefix='item_transfer_choise_char'):
    to_search: bool = False
    to_list: bool = False
    to_my_char: bool = False

class ItemTransferBackCall(CallbackData, prefix='item_transfer_back'):
    where: str

class ItemTransferCharIdCall(CallbackData, prefix='item_transfer_char_id'):
    char_id: int

class ItemTransferCharPageCall(CallbackData, prefix='item_transfer_page'):
    page: int

class ItemTransferActionCall(CallbackData, prefix='item_transfer_action'):
    action: Literal['+', '-']
    side: int

class ItemTransferTradeStatusCall(CallbackData, prefix='item_transfer_trade_status'):
    status: ItemTransferStatusEnum

class ItemTransferItemIdCall(CallbackData, prefix='item_transfer_item_id'):
    item_id: int
    side: int

class ItemTransferItemPageCall(CallbackData, prefix='item_transfer_item_page'):
    page: int
    side: int



class InfoTransferStartCall(CallbackData, prefix='info_transfer_start'):
    to_create: bool = False
    to_faq: bool = False
    to_reload: bool = False

class InfoTransferBackCall(CallbackData, prefix='info_transfer_back'):
    where: str

class InfoTransferPageCall(CallbackData, prefix='info_transfer_page'):
    page: int

class InfoTransferInfoCall(CallbackData, prefix='info_transfer_info'):
    transfer_id: int

class InfoTransferStatusCall(CallbackData, prefix='info_transfer_status'):
    status: ItemTransferStatusEnum

class InfoTransferSortedCall(CallbackData, prefix='info_transfer_sorted'):
    status: str

class InfoTransferSearchCall(CallbackData, prefix='info_transfer_search'):
    search_type: str
    
class InfoTransferActionCall(CallbackData, prefix='info_transfer_action'):
    transfer_id: int
    to_new_status: bool = False
    to_redact: bool = False
    to_complete: bool = False
    to_delete: bool = False
    new_status: str | None = None
