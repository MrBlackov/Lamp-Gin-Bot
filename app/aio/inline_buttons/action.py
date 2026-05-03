from app.aio.cls.callback.action import ActionBackCall, MenuCall, ActionCall, ActionRedactCall, LookAroundCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.enum_type.tags import ActionTags
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.logic.actions import ActionBase
from app.db.models.char import ExistenceDB

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
        self.builder.button(text='📊 Статистика', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='🌞 Проснуться', callback_data=ActionCall(tag=ActionTags.wake_up, tg_id=self.tg_id))
        return self.builder.as_markup()

    def stop(self):
        self.builder.button(text='📊 Статистика', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='⏸️ Остановиться', callback_data=ActionCall(tag=ActionTags.stop, tg_id=self.tg_id))
        return self.builder.as_markup()

    def stats(self):
        self.builder.button(text='🔁 Обновить', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='⏸️ Остановиться', callback_data=ActionCall(tag=ActionTags.stop, tg_id=self.tg_id))
        return self.builder.as_markup()    
      
    def time_action(self, tag: str, emodzi: str, action_text: str, where: str, minute: int | None = None):      
        self.builder.button(text='⏱️ Изменить время', callback_data=ActionRedactCall(tag=tag, to_time=True, tg_id=self.tg_id)).as_markup()
        self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where=where, is_details=True, tg_id=self.tg_id)).as_markup()
        self.builder.button(text=emodzi + ' ' + action_text, callback_data=ActionCall(tag=tag, step=2, minute=minute, tg_id=self.tg_id)).as_markup()
        return self.builder.adjust(1, 2).as_markup()

    def lookaround(self, results: list[tuple[ExistenceDB | None, ActionBase | None]]):        
        for exist, action in results:
            self.builder.button(text=f'{action.emodzi} {exist.full_name} {action.action_text}', callback_data=LookAroundCall(tg_id=self.tg_id))
        self.builder.button(text='👁️ Посмотреть ещё раз', callback_data=ActionCall(tag=ActionTags.lookaround, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where='actions', is_details=True, tg_id=self.tg_id)).as_markup()
        return self.builder.adjust(1).as_markup()


