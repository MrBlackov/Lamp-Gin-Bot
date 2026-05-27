from aiogram.fsm.context import FSMContext
from app.logged.botlog import logs, log
from app.logged.infolog import infolog
from app.aio.msg.base import UserText, ChatText
from app.aio.msg.utils import TextHTML
from app.service.base import BaseService 
from app.interlayer.main import ChatLayer, UserLayer, ChatDB
from app.aio.cls.fsm.utils import UserFSM, ChatFSM
from app.aio.inline_buttons.main import ChatIKB, MenuIKB
from app.aio.cls.fsm.main import ChatState
from app.exeption.main import MainQuantityLessSixTeen, MainQuantityMaxTime
from app.enum_type.bd import TgType
from app.exeption.main import MainQuantityFloat, MainQuantityLessSixTeen, MainQuantityNoInt

class UserService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = UserLayer(tg_id)
        self.state = UserFSM(state)
        self.text = UserText
        self.menu_ikb = MenuIKB(tg_id)

    def menu(self):
        return '🏠 Главное меню',  self.menu_ikb.menu()

    async def get_info(self, user_id: int | None = None):
        
        layer = await self.layer.get_char_info()
        text = self.text(layer.user.tg_user, layer.user).text
        return text

    async def get_logs(self):
        results, all, msg = await log.send_all_log_files()
        return f'🗂️ Логи отправлены: {results}/{all} ({TextHTML('Файлы').href(f'https://t.me/c/{str(msg.chat.id).strip('-100')}/177015/{msg.message_id}')})', None

class ChatService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = ChatLayer(tg_id)
        self.state = ChatFSM(state)
        self.text = ChatText
        self.IKB = ChatIKB(tg_id)

    async def menu(self, tg_id: int):
        chat = await self.layer.setting(tg_id)
        return self.text(chat.tg_chat, chat, self.message).text, self.menu_ikb(chat)
    
    def menu_ikb(self, chat: ChatDB):
        return self.IKB.menu(chat.id, 
                             chat.setting.is_msg_delete, 
                             chat.setting.greetings_new_members, 
                             chat.setting.receive_drops, 
                             chat.tg_chat.tg_type == TgType.PRIVATE, 
                             is_default_text=chat.setting.is_default, 
                             is_chat_have_topic=self.message.chat.is_forum, 
                             main_topic_id=chat.setting.main_topic_id)

    async def redact_text_parametrs(self, chat_id: int, parametr: str, msg):
        await self.state.set_state(ChatState.redact_text_parametr)
        await self.state.update_data(chat_id=chat_id, msg=msg, parametr=parametr)
        return '✒️ Укажите новое значение', self.IKB.redact_text('menu')

    async def new_msg_delete_time(self, new_value):
        parametr = await self.state.get_value('parametr')
        if parametr == 'msg_delete_time':
            new_value = self.is_natural_int(new_value)
            if new_value < 60:
                raise MainQuantityLessSixTeen(f'This user(tg_id={self.tg_id}) try set msg delete time less than 60 second')
            if new_value > 170_000:
                raise MainQuantityMaxTime(f'This user(tg_id={self.tg_id}) try set msg delete time more than 170.000 second')
        if parametr == 'main_topic_id':
            new_value = self.is_natural_int(new_value)
        chat_id = await self.state.get_value('chat_id')
        chat = await self.layer.redact_parametrs(chat_id, new_data={parametr: new_value})
        return self.text(chat.tg_chat, chat, self.message).text, self.menu_ikb(chat)

    async def redact_is_bool_parametrs(self, chat_id: int, new_value, parametr: str):
        chat = await self.layer.redact_parametrs(chat_id, new_data={parametr: new_value})
        return self.text(chat.tg_chat, chat, self.message).text, self.menu_ikb(chat)

    async def send_greetings_new_member(self, chat_id: int, full_name: str):
        chat = await self.layer.setting(chat_id)
        if chat.setting.greetings_new_members:
            text = chat.setting.greetings_text.format(full_name=full_name)
            await self.bot.send_message(chat_id, text, message_thread_id=chat.setting.main_topic_id)

