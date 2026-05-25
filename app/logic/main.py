from app.db.metods.adds import add_chat_setting
from app.db.metods.gets import get_chat_for_id, get_chat_for_tg_id, get_chat_setting_for_id, ChatDB
from app.db.metods.updates import update_chat_by_setting, update_chat_setting_by_id, update_chat_setting_by_chat_id

class ChatLogic:
    async def setting(self, tg_id: int):
        chat = await get_chat_for_tg_id(tg_id)     
        return chat
 
    async def info(self, chat_id: int):
        chat = await get_chat_for_id(chat_id)
        return chat
    
    async def redact_parametrs(self, chat_id: int, new_data: dict):
        setting = await update_chat_setting_by_chat_id(chat_id=chat_id, new_data=new_data)
        return await self.info(setting.chat_id)
    
    async def redact_msg_delete_time(self, chat_id: int, msg_delete_time: int):
        return await self.redact_parametrs(chat_id=chat_id, new_data={'msg_delete_time': msg_delete_time})

    