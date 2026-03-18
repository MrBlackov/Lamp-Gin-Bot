from app.aio.config import bot
from app.interlayer.message import MessageLayer, NoDeleteMessageError
import asyncio

class MessageUtils:
    def __init__(self, tg_chat_id: int | None = None):
        self.layer = MessageLayer(tg_chat_id)
        self.jobstore = 'msg_delete'
        self.tg_chat_id = tg_chat_id
    
    def use(tg_chat_id: int):
        return MessageUtils(tg_chat_id)

    async def delete_for_time(self):
        msgs = await self.layer.get_message_to_delete()
        results = {}
        for msg in msgs:
            try:
                delete_msg = await bot.delete_message(msg.chat_tg_id, msg.msg_id)
                results[msg.id] = delete_msg
            except Exception as e:
                print('MessageUtilsDeleter: ', e)
                results[msg.id] = True
        result_ids = [m for m, is_delete in results.items() if is_delete]
        await self.layer.delete_message_db(result_ids)
        print('Удалено сообщений: ', len(result_ids))


    async def add_to_delete(self, msg_id: int, is_delete: bool = True):
        return await self.layer.add_message_to_delete(msg_id)

    async def update_time_default(self, msg_id: int):
        return await self.layer.update_time(self.tg_chat_id, msg_id)

    async def run_deleter_job(self, seconds: int = 5):
        while True:
            try:
                await self.delete_for_time()
            except Exception as e:
                print('MessageUtilsRunner: ', e)
                return True
            finally:
                await asyncio.sleep(5)
                

