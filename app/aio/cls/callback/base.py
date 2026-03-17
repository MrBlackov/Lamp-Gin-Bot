from aiogram.filters.callback_data import CallbackData

class BaseCall(CallbackData, prefix='base'):
    tg_id: int