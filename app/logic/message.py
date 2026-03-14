from app.db.metods.unique import get_message_to_delete
from app.db.metods.adds import add_message_delete, MessageDB
from app.db.metods.gets import get_message
from app.db.metods.updates import update_message
from app.db.metods.deletes import delete_messages

class MessageLogic:
    async def get_to_delete(self):
        msgs: list[MessageDB] = await get_message_to_delete()
        await self.delete_messages(ids=[m.id for m in msgs if m.is_delete == False])
        return [m for m in msgs if m.is_delete == True]
    
    async def add(self, tg_chat_id: int, msg_id: int, time_delete, is_delete: bool = True):
        return await add_message_delete(tg_chat_id, msg_id, time_delete, is_delete)

    async def update_time(self, tg_chat_id: int, msg_id: int, time_delete):
        msg = await self.get(tg_chat_id, msg_id)
        if msg == None:
            return await self.add(tg_chat_id, msg_id, time_delete)
        return await update_message(filters={'chat_tg_id':tg_chat_id, 'msg_id':msg_id}, new_data={'time_delete':time_delete})
    
    async def get(self, tg_chat_id: int, message_id: int):
        return await get_message(tg_chat_id, message_id)

    async def delete_messages(self, ids: list[int]):
        return await delete_messages(ids=ids)