from aiogram.filters.callback_data import CallbackData

class CraftIdCall(CallbackData, prefix='craft_id'):
    craft_id: int

class CraftBackCall(CallbackData, prefix='craft_back'):
    where: str

class CraftPageCall(CallbackData, prefix='craft_page'):
    page: int

class CraftActionCall(CallbackData, prefix='craft_action'):
    to_craft_hiden: bool = False
    craft_hiden: bool = False
    to_faq: bool = False
    faq: str | None = None
    to_craft: bool = False
    to_send: bool = False
    to_time: bool = False

class CraftCreateActionCall(CallbackData, prefix='craft_action_hiden'):
    item_type: str
    action: str

class CraftItemPagesCall(CallbackData, prefix='craft_item_pages'):
    page: int
    item_type: str

class CraftItemIdCall(CallbackData, prefix='craft_item_id'):
    item_id: int