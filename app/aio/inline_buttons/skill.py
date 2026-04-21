from app.aio.cls.callback.skill import SkillBackCall, SkillCall, SkillPageCall, MenuCall
from app.db.models.item import ItemDB, SkillDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class SKillIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=SkillBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def skills(self, skills: list[SkillDB], page: int, max_page: int, where: str | None = None):
        k = 0
        for skill in skills:
            k += 1
            self.builder.button(text=f'{k}', callback_data=SkillCall(skill_id=skill.id, tg_id=self.tg_id))
        self.builder.adjust(5, repeat=True)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=SkillPageCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=SkillPageCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️', callback_data=SkillBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()     





