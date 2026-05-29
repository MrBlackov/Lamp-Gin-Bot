from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from app.aio.cls.callback.main import ChatSettingActionCall, ChatBackCall, MenuCall
from app.aio.config import wiki

class MenuIKB(BotIKB):
    def menu(self):
        self.builder.button(text='👑 Действующий персонаж', callback_data=MenuCall(where='mychar', tg_id=self.tg_id))
        self.builder.button(text='👥 Персонажи', callback_data=MenuCall(where='mychars', tg_id=self.tg_id))
        self.builder.button(text='😎 Друзья', callback_data=MenuCall(where='myfriends', tg_id=self.tg_id))
        self.builder.button(text='⚙️ Настройки аккаунта', callback_data=MenuCall(where='user_setting', tg_id=self.tg_id))
        self.builder.button(text='📦 Список всех предметов в игре', callback_data=MenuCall(where='items', tg_id=self.tg_id))
        self.builder.button(text='💡 Список всех навыков в игре', callback_data=MenuCall(where='skills', tg_id=self.tg_id))
        self.builder.button(text='📚 Получить справку', callback_data=MenuCall(where='help', tg_id=self.tg_id))
        self.builder.button(text='📖 Вики', url=wiki)
        return self.builder.adjust(1).as_markup()      

class ChatIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=ChatBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def menu(self, 
             chat_id: int, 
             is_msg_delete: bool, 
             is_greetings_new_members: bool = False, 
             is_receive_drops: bool = False, 
             is_private: bool = False, 
             is_default_text: bool | None = None,
             is_chat_have_topic: bool = False, 
             main_topic_id: int | None = None):
        if is_msg_delete == False:
            self.builder.button(text='✅ Включить удаление сообщений', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='is_msg_delete', bool_parametrs=True, to_redact_bool_parametr=True, tg_id=self.tg_id))
        else:    
            self.builder.button(text='⏱️ Указать время удаления', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='msg_delete_time', to_redact_text_parametr=True, tg_id=self.tg_id))
            self.builder.button(text='❌ Выключить удаление сообщений', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='is_msg_delete', bool_parametrs=False, to_redact_bool_parametr=True, tg_id=self.tg_id))
        if not is_private:
            self.builder.button(text='❌ Выключить приветствие новых участников' if is_greetings_new_members else '✅ Включить приветствие новых участников', 
                                callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='greetings_new_members', bool_parametrs=not is_greetings_new_members, to_redact_bool_parametr=True, tg_id=self.tg_id))
            if is_greetings_new_members:
                self.builder.button(text='✏️ Изменить текст приветствия', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='greetings_text', to_redact_text_parametr=True, tg_id=self.tg_id))
                if not is_default_text:
                    self.builder.button(text='❌ Вернуть к стандартному тексту', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='greetings_text', bool_parametrs=None, to_redact_bool_parametr=True, tg_id=self.tg_id))
            self.builder.button(text='❌ Выключить получение дропов' if is_receive_drops else '✅ Включить получение дропов', 
                                callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='receive_drops', bool_parametrs=not is_receive_drops, to_redact_bool_parametr=True, tg_id=self.tg_id))
            if is_chat_have_topic:
                self.builder.button(text=('✏️ Изменить главный топик' if main_topic_id else '➕ Добавить главный топик'), callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='main_topic_id', to_redact_text_parametr=True, tg_id=self.tg_id))
                if main_topic_id:
                    self.builder.button(text='🗑️ Убрать главный топик', callback_data=ChatSettingActionCall(chat_id=chat_id, parametrs='main_topic_id', bool_parametrs=None, to_redact_bool_parametr=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def redact_text(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ChatBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
