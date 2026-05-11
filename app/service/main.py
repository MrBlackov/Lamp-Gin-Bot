from aiogram.fsm.context import FSMContext
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.base import UserText, ChatText
from app.aio.msg.utils import TextHTML
from app.service.base import BaseService 
from app.interlayer.main import ChatLayer, UserLayer
from app.aio.cls.fsm.utils import UserFSM, ChatFSM
from app.aio.inline_buttons.main import ChatIKB, MenuIKB
from app.aio.cls.fsm.main import ChatState
from app.exeption.main import MainQuantityLessSixTeen, MainQuantityMaxTime

class UserService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
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

class ChatService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = ChatLayer(tg_id)
        self.state = ChatFSM(state)
        self.text = ChatText
        self.IKB = ChatIKB(tg_id)

    async def menu(self, tg_id: int):
        chat = await self.layer.setting(tg_id)
        return self.text(chat.tg_chat, chat).text, self.IKB.menu(chat.id, chat.setting.is_msg_delete)
    
    async def redact_msg_delete_time(self, chat_id: int, msg):
        await self.state.set_state(ChatState.msg_delete_time)
        await self.state.update_data(chat_id=chat_id, msg=msg)
        return '✒️ Укажите новое время удаления сообщения', self.IKB.back('menu')

    async def new_msg_delete_time(self, new_time: int):
        if new_time < 120:
            raise MainQuantityLessSixTeen(f'This user(tg_id={self.tg_id}) try set msg delete time less than 60 second')
        if new_time > 170_000:
            raise MainQuantityMaxTime(f'This user(tg_id={self.tg_id}) try set msg delete time more than 170.000 second')
        chat_id = await self.state.get_value('chat_id')
        chat = await self.layer.redact_msg_delete_time(chat_id, new_time)
        return self.text(chat.tg_chat, chat).text, self.IKB.menu(chat.id, chat.setting.is_msg_delete)

    async def redact_is_msg_delete(self, chat_id: int, is_msg_delete: bool):
        chat = await self.layer.redact_is_msg_delete(chat_id, is_msg_delete)
        return self.text(chat.tg_chat, chat).text, self.IKB.menu(chat.id, chat.setting.is_msg_delete)

