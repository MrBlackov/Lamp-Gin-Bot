from app.aio.cls.callback.action import ActionBackCall, MenuCall, ActionCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.enum_type.tags import ActionTags
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class ActionIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where=where, is_details=True, tg_id=self.tg_id)).as_markup()

    def actions(self, actions: dict[str, list], is_details: bool = True):
        for tag, text in actions.items():
            self.builder.button(text=(' '.join(text) if not(is_details) else text[0]), callback_data=ActionCall(tag=tag, tg_id=self.tg_id))
        self.builder.adjust((3 if is_details else 1), repeat=True)
        self.builder.row(InlineKeyboardButton(text=('➖ Менее подробнее' if not(is_details) else '➕ Подробнее'), callback_data=ActionBackCall(where='actions', is_details=not(is_details), tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
 
    def wake_up(self):
        self.builder.button(text='🌞 Проснуться', callback_data=ActionCall(tag=ActionTags.wake_up, tg_id=self.tg_id).pack())
        return self.builder.as_markup()

    def stop(self):
        self.builder.button(text='⏸️ Остановиться', callback_data=ActionCall(tag=ActionTags.stop, tg_id=self.tg_id).pack())
        return self.builder.as_markup()

