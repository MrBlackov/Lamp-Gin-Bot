from app.aio.cls.callback.base import BaseCall
from typing import Any, Literal

class ToErrorFAQCall(BaseCall, prefix='to_error_faq'):
    code: str


class MenuFAQCall(BaseCall, prefix='menu_faq'):
    to_new_char: bool = False
    to_help_cmd: bool = False

    