from aiogram.utils.keyboard import InlineKeyboardBuilder

class BotIKB:
    def __init__(self, tg_id: int):
        self.builder = InlineKeyboardBuilder()
        self.tg_id = tg_id
 
    def another_tg_id(self, tg_id: int):
        self.tg_id = tg_id
        return self
        
    