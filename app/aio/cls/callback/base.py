from aiogram.filters.callback_data import CallbackData

class BaseCall(CallbackData, prefix='base'):
    tg_id: int

class MenuCall(BaseCall, prefix='menu'):
    where: str
    