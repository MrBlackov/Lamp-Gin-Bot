from app.aio.cls.callback.skill import SkillBackCall, SkillCall, SkillPageCall, MenuCall
from app.aio.cls.callback.action import ActionCall
from app.db.models.item import ItemDB, SkillDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.msg.utils import TextHTML
from app.logic.actions import ActionSelf
from app.enum_type.tags import SkillTags

class SKillIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=SkillBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def skills(self, skills: list[SkillDB], page: int, max_page: int, where: str | None = None):
        for skill in skills:
            if skill.sketch.is_hide:
                continue
            if skill.sketch.custom_emodzi_id:
                button_text = {'text':  f' {skill.sketch.name} - {TextHTML.float_format(skill.level, 5)} ур.', 'icon_custom_emoji_id': skill.sketch.custom_emodzi_id}
            else:
                button_text = {'text': f'{skill.sketch.emodzi} {skill.sketch.name} - {TextHTML.float_format(skill.level, 5)} ур.'}
            self.builder.button(**button_text, callback_data=SkillCall(skill_id=skill.id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=SkillPageCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=SkillPageCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=SkillBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()     

    def skill(self, skill: SkillDB, where: str = 'myskills'):
        action = ActionSelf.item_action().get(skill.sketch.tag)
        if action:
            self.builder.button(text=action.text(), callback_data=ActionCall(tag=action.tag, tg_id=self.tg_id))
        elif skill.sketch.tag == SkillTags.craft:
            self.builder.button(text=f'{skill.sketch.emodzi} Скрафтить', callback_data=MenuCall(where='crafts', tg_id=self.tg_id))
        self.builder.button(text=f'↩️ Назад', callback_data=SkillBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
        



