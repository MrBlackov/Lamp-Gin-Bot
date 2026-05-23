from app.aio.cls.callback.stats import MenuCall, StatsBackCall, TopSkillCall, TopActionCall, StatsActionCall
from app.db.models.skill import SkillSketchDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class StatsIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id)).as_markup()
   
    def topskills(self, skills: list[SkillSketchDB], where: str):
        for skill in skills:
            self.builder.button(**skill.button_text, callback_data=TopSkillCall(skill_tag=skill.tag, tg_id=self.tg_id))
        self.builder.adjust(2)
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def tops(self):
        self.builder.button(text='💡 Навыки', callback_data=TopActionCall(to_skill=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def topskill(self, skill_tag: str, where: str):
        self.builder.button(text='🔄️ Обновить', callback_data=TopSkillCall(skill_tag=skill_tag, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=StatsBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()