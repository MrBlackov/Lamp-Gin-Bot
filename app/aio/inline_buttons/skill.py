from app.aio.cls.callback.skill import SkillBack
from app.db.models.item import ItemDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class SKillIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=SkillBack(where=where, tg_id=self.tg_id)).as_markup()





