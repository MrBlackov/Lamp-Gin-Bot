from app.aio.cls.callback.faq import ToErrorFAQCall, MenuFAQCall, MenuCall
from app.db.models.item import ItemDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from app.aio.config import wiki

class FaqIKB(BotIKB):
    def to_error_faq(self, code: str):
        return self.builder.button(text='❓ Подробнее', callback_data=ToErrorFAQCall(code=code, tg_id=self.tg_id)).as_markup()
   
    def to_start(self):
        self.builder.button(text='👤 Создать персонажа', callback_data=MenuFAQCall(to_new_char=True, tg_id=self.tg_id))
        self.builder.button(text='🏠 Меню', callback_data=MenuCall(where='menu', tg_id=self.tg_id))
        self.builder.button(text='📖 Вики', web_app=WebAppInfo(url=wiki))
        return self.builder.adjust(1).as_markup()
        
    def help(self):
        self.builder.button(text='📰 Актуальные новости по боту', url='https://t.me/oldneal')
        self.builder.button(text='📖 Вики', web_app=WebAppInfo(url=wiki))
        return self.builder.adjust(1).as_markup()
