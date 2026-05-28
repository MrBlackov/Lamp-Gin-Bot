from app.db.models.main import UserDB, TgUserDB, ChatDB, TgChatDB
from app.aio.msg.utils import TextHTML

class UserText:
    def __init__(self, tg_user: TgUserDB, user: UserDB):
        self.user = user
        self.tg_user = tg_user

    @property
    def text(self):
        return TextHTML(f'{self.tg_user.fullname}').href(f'tg://openmessage?user_id={self.user.tg_id}') + TextHTML('\n'.join([
            f'🔰 user_id: {self.user.id}',
            f'💠 tg_id: {self.user.tg_id}',
            f'📧 username: {self.tg_user.username if self.tg_user.username else "❌"}'
        ])).blockquote()

class ChatText:
    def __init__(self, tg_chat: TgChatDB, chat: ChatDB, message = None):
        self.chat = chat
        self.tg_chat = tg_chat
        self.message = message

    @property
    def text(self):
        return TextHTML(f'{self.tg_chat.fullname}').href(f'tg://openmessage?user_id={self.chat.tg_id}') + TextHTML('\n'.join([
            f'🔰 chat_id: {self.chat.id}',
            f'💠 tg_id: {self.chat.tg_id}',
            f'📧 username: {self.tg_chat.username if self.tg_chat.username else "❌"}',
            f'📂 Тип: {self.tg_chat.tg_type.to_ru(self.tg_chat.tg_type)}'
        ]) + f'{f'\n🗑️ Время удаления сообщений: {self.chat.setting.msg_delete_time} с.' if self.chat.setting.is_msg_delete else ''}' + (f'\n📍 Главный топик: {self.chat.setting.main_topic_id if self.chat.setting.main_topic_id else '❌'}' if self.message.chat.is_forum else '')).blockquote() + ('\n\n👋 Приветствие' + TextHTML(self.chat.setting.greetings_text).blockquote() if self.chat.setting.greetings_new_members else '')