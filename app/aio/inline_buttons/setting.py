from app.aio.cls.callback.setting import SettingBackCall, SettingRedactCall, SettingActionCall
from app.aio.cls.callback.faq import FAQCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from app.aio.msg.utils import TextHTML
from app.logic.settings import SettingSelf, SettingValueBase

class SettingIKB(BotIKB):
    def back(self, where: str, type: str):
        return self.builder.button(text='↩️ Назад', callback_data=SettingBackCall(where=where, type=type, tg_id=self.tg_id)).as_markup()

    def setting(self, setting: list[SettingValueBase], type: str):
        for a in setting:
            self.builder.button(text=a.button_text, callback_data=SettingRedactCall(tag=a.tag, type=type, tg_id=self.tg_id))
        values = {a.tag:a.value for a in setting}
        self.builder.adjust(1)
        self.builder.row(InlineKeyboardButton(text='📑 Свой шаблон', callback_data=SettingActionCall(to_insert_json=True, type=type, tg_id=self.tg_id).pack()),
                         InlineKeyboardButton(text='📋 Копировать', copy_text=CopyTextButton(text=f'{values}')), width=2)  
        self.builder.row(InlineKeyboardButton(text='🗑️ По умолчанию', callback_data=SettingActionCall(to_default_values=True, type=type, tg_id=self.tg_id).pack()))  
        self.builder.row(InlineKeyboardButton(text='ℹ️ Помощь', callback_data=FAQCall(faq='setting', to_answer_callback=False, tg_id=self.tg_id).pack()))  
        return self.builder.as_markup()   
