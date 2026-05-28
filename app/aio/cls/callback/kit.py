from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Literal

class KitIdCall(BaseCall, prefix='kit_id'):
    kit_id: int
    is_new: bool = False

class KitBackCall(BaseCall, prefix='kit_back'):
    where: str

class KitActionCall(BaseCall, prefix='kit_action'):
    kit_id: int | None = None
    to_enter_code: bool = False
    to_get_kit: bool = False
    to_arhiv: bool = False
    to_save: bool = False

