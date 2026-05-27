from app.aio.cls.callback.drop import DropBackCall, DropActionCall, DropItemCall
from app.aio.cls.callback.faq import FAQCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from app.aio.msg.utils import TextHTML
from app.db.models.item import ItemDB

class DropIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=DropBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def check(self, is_open: bool = False):
        return self.builder.button(text=('👀 Найти другой сундук' if is_open else '👀 Посмотреть еще раз'), callback_data=DropBackCall(where='drop', tg_id=self.tg_id)).as_markup()
    
    def open(self, drop_id: int):
        return self.builder.button(text='🔑 Открыть', callback_data=DropActionCall(to_open=True, drop_id=drop_id, tg_id=self.tg_id, is_check=False)).as_markup()

    def items(self, drop_id: int, items: list[ItemDB]):
        for item in items:
            self.builder.button(**item.button_text, callback_data=DropItemCall(sketch_id=item.sketch.id, quantity=item.quantity, drop_id=drop_id, tg_id=self.tg_id, is_check=False))
        return self.builder.adjust(1).as_markup()

