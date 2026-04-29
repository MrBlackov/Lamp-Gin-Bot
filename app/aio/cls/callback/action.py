from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class ActionBackCall(BaseCall, prefix='action_back'):
    where: str
    is_details: bool = False

class ActionCall(BaseCall, prefix='action'):
    tag: str

    