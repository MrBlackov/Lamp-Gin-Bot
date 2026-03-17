from app.aio.cls.callback.faq import ToErrorFAQCall, MenuFAQCall
from app.db.models.item import ItemDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class FaqIKB(BotIKB):
    def to_error_faq(self, code: str):
        return self.builder.button(text='❓ Подробнее', callback_data=ToErrorFAQCall(code=code, tg_id=self.tg_id)).as_markup()
   
    def to_start(self):
        self.builder.button(text='👤 Создать персонажа', callback_data=MenuFAQCall(to_new_char=True, tg_id=self.tg_id))
        self.builder.button(text='📜 Узнать список команд', callback_data=MenuFAQCall(to_help_cmd=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
        

