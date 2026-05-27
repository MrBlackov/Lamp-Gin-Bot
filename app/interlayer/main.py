from app.interlayer.base import BaseLayer
from app.logic.main import ChatLogic, ChatDB

class UserLayer(BaseLayer):
    pass

class ChatLayer(BaseLayer):
    def __init__(self, tg_id: int):
        super().__init__(tg_id)
        self.logic = ChatLogic()

    def default_greetings_text(self, chat: ChatDB):  
        chat.setting.greetings_text = chat.setting.greetings_text if chat.setting.greetings_text else '👋 Рады видеть тебя тут, {full_name}! \n\n❔ А у тебя уже есть, персонаж в Лампе? Если нет, то быстрее создавай его, используя команду - /newchar'
        chat.setting.is_default = True if chat.setting.greetings_text == '👋 Рады видеть тебя тут, {full_name}! \n\n❔ А у тебя уже есть, персонаж в Лампе? Если нет, то быстрее создавай его, используя команду - /newchar' else False
        return chat

    async def setting(self, tg_id: int):
        chat = await self.logic.setting(tg_id)
        return self.default_greetings_text(chat)

    async def redact_parametrs(self, chat_id: int, new_data: dict):
        chat = await self.logic.redact_parametrs(chat_id, new_data)
        return self.default_greetings_text(chat)
 
    async def redact_msg_delete_time(self, chat_id: int, msg_delete_time: int):
        chat = await self.logic.redact_msg_delete_time(chat_id, msg_delete_time)
        return self.default_greetings_text(chat)