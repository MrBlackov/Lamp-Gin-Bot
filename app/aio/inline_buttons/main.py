from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.callback.main import ChatSettingActionCall, ChatBackCall, MenuCall

class ChatIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=ChatBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def menu(self, chat_id: int, is_msg_delete: bool):
        if is_msg_delete == False:
            return self.builder.button(text='✅ Включить удаление сообщений', 
                                       callback_data=ChatSettingActionCall(chat_id=chat_id, is_msg_delete=True, tg_id=self.tg_id)).as_markup()
        self.builder.button(text='⏱️ Указать время удаления', callback_data=ChatSettingActionCall(chat_id=chat_id, to_msg_delete_time=True, tg_id=self.tg_id))
        self.builder.button(text='❌ Выключить удаление сообщений', callback_data=ChatSettingActionCall(chat_id=chat_id, is_msg_delete=False, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
