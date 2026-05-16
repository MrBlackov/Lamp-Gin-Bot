from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal
import json

class ActionBackCall(BaseCall, prefix='action_back'):
    where: str
    is_details: bool = False

class ActionCall(BaseCall, prefix='action'):
    tag: str
    step: int = 1
    minute: int | None = None
    item_id: int | None = None

class ThrowItemCall(ActionCall, prefix='throw_item'):
    quantity: int = 1
    purpose_char_id: int | None = None

class ActionRedactCall(BaseCall, prefix='action_redact'):
    to_time: bool = False
    to_item: bool = False
    tag: str
    to_stats: bool = False
    to_del_timer: bool = False

class LookAroundCall(BaseCall, prefix='look_around'):
    pass

class ThrowItemQuantityCall(ThrowItemCall, prefix='throw_item_quantity'):
    pass

class ActionPageCall(BaseCall, prefix='action_page'):
    page: int
    tag: str
