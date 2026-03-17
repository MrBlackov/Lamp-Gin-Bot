from aiogram.utils.keyboard import InlineKeyboardBuilder

class BotIKB:
    def __init__(self, tg_id: int):
        self.builder = InlineKeyboardBuilder()
        self.tg_id = tg_id