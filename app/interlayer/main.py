from app.interlayer.base import BaseLayer
from app.logic.main import ChatLogic

class UserLayer(BaseLayer):
    pass

class ChatLayer(BaseLayer):
    def __init__(self, tg_id: int):
        super().__init__(tg_id)
        self.logic = ChatLogic()

    async def setting(self, tg_id: int):
        return await self.logic.setting(tg_id)

    async def redact_is_msg_delete(self, chat_id: int, is_msg_delete: bool):
        return await self.logic.redact_is_msg_delete(chat_id, is_msg_delete)
 
    async def redact_msg_delete_time(self, chat_id: int, msg_delete_time: int):
        return await self.logic.redact_msg_delete_time(chat_id, msg_delete_time)