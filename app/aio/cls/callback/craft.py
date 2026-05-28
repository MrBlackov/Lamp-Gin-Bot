from app.aio.cls.callback.base import BaseCall, MenuCall

class CraftIdCall(BaseCall, prefix='craft_id'):
    craft_id: int

class CraftBackCall(BaseCall, prefix='craft_back'):
    where: str

class CraftPageCall(BaseCall, prefix='craft_page'):
    page: int

class CraftActionCall(BaseCall, prefix='craft_action'):
    to_craft_hiden: bool = False
    craft_hiden: bool = False
    to_faq: bool = False
    faq: str | None = None
    to_craft: bool = False
    to_send: bool = False
    to_time: bool = False
    to_craft_quantity: bool = False
    craft_id: int | None = None
    redact_hide: bool = False 
    hide: bool | None = None
    
class CraftUseCall(BaseCall, prefix='craft_use'):
    craft_id: int
    quantity: int = 1

class CraftCreateActionCall(BaseCall, prefix='craft_action_hiden'):
    item_type: str
    action: str

class CraftItemPagesCall(BaseCall, prefix='craft_item_pages'):
    page: int
    item_type: str

class CraftItemIdCall(BaseCall, prefix='craft_item_id'):
    item_id: int

class CraftAdminACtionCall(BaseCall, prefix='craft_admin_action'):
    craft_id: int
    to_redact: bool = False
    to_create: bool | None = None  