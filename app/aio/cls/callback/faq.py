from aiogram.filters.callback_data import CallbackData
from typing import Any, Literal

class ToErrorFAQCall(CallbackData, prefix='to_error_faq'):
    code: str


class MenuFAQCall(CallbackData, prefix='menu_faq'):
    to_new_char: bool = False
    to_help_cmd: bool = False

    