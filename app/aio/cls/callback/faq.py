from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class ToErrorFAQCall(BaseCall, prefix='to_error_faq'):
    code: str


class MenuFAQCall(BaseCall, prefix='menu_faq'):
    to_new_char: bool = False
    to_help_cmd: bool = False
    to_new_char_action: bool = False

class FAQCall(BaseCall, prefix='faq'):
    faq: str    
    