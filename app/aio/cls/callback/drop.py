from app.aio.cls.callback.base import BaseCall, MenuCall, BackCall
from typing import Any, Literal

class DropBackCall(BackCall, prefix='drop_back'):
    pass

class DropCall(BaseCall, prefix='drop'):
    drop_id: int

class DropActionCall(DropCall, prefix='drop_action'):
    to_open: bool | None = None

class DropItemCall(DropCall, prefix='drop_item'):
    sketch_id: int
    quantity: int

