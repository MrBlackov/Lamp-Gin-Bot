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
    to_faq_ingredient: bool = False
    to_faq_tool: bool = False

class CraftActionHidenCall(CallbackData, prefix='craft_action_hiden'):
    is_ingredient: bool = False
    is_tool: bool = False
    action: str


