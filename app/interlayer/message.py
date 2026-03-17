from app.logged.infolog import infolog
from app.aio.config import admins, bot, newspaper_id
from app.interlayer.main import ChatLogic
from datetime import datetime, timedelta, timezone
from app.exeption.main import NoDeleteMessageError
from app.logic.message import MessageDB, MessageLogic

class MessageLayer:
    def __init__(self, tg_chat_id: int | None = None, chat_id: int | None = None):
        self.chat_id = chat_id
        self.tg_chat_id = tg_chat_id
        self.chat_logic = ChatLogic()
        self.logic = MessageLogic()

    async def get_chat_setting(self, chat_id: int | None = None):
        if self.tg_chat_id:
            self.chat = await self.chat_logic.setting(self.tg_chat_id)
        else:
            if chat_id == None:
                chat_id = self.chat_id
            self.chat = await self.chat_logic.info(chat_id)
        return self

    async def get_message_to_delete(self) -> list[MessageDB]:
        return await self.logic.get_to_delete()

    async def delete_message_db(self, ids: list[int]):
        return await self.logic.delete_messages(ids=ids)
    
    async def time_delete(self):
        await self.get_chat_setting()
        if self.chat.setting.is_msg_delete == False:
            raise NoDeleteMessageError(f':)')
        return self.times()

    def times(self):
        return datetime.now() + timedelta(seconds=self.chat.setting.msg_delete_time)

    async def add_message_to_delete(self, msg_id: int):
        await self.get_chat_setting()
        if self.chat.setting.is_msg_delete:
            msg = await self.logic.get(self.chat.tg_id, msg_id)
            return await self.logic.add(self.chat.tg_id, msg_id, self.times()) if msg == None else await self.logic.update_time(self.tg_chat_id, msg_id, self.times())

    async def update_time(self, tg_chat_id: int, msg_id: int):
        await self.get_chat_setting()
        if self.chat.setting.is_msg_delete:
            return await self.logic.update_time(tg_chat_id, msg_id, self.times())