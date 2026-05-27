from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.drop import DropIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.setting import TextHTML
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from app.interlayer.drop import DropLayer
from app.aio.cls.fsm.utils import DropFSM

class DropService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = DropLayer(tg_id)
        self.state = DropFSM(state)
        self.IKB = DropIKB(tg_id)

    async def get_drop(self):
        drop = await self.layer.get_drop(self.message.chat.id)
        if drop == None:
            return '❌ Никаких сундуков в округе', self.IKB.check()
        return '📦 Найден сундук', self.IKB.open(drop.id)

    async def open_drop(self, drop_id: int):
        items = await self.layer.open_drop(drop_id)
        if items and len(items) > 0:
            return '🔓 Сундук открыт', self.IKB.items(drop_id, items)
        return '😢 Сундук пустой', self.IKB.check(is_open=True)
    
    async def create_drop(self, chat_tg_id: int):
        return await self.layer.create_drop(chat_tg_id, coins=await self.bot.get_chat_member_count(chat_tg_id))

    async def runner(self):
        while True:
            sleep_time = 20
            try:
                now = self.datetime.datetime.now()
                drops = await self.layer.get_drops(time=now, operator='<=', is_open=False)
                if len(drops) > 0:
                    await self.texts_boardcast([(drop.chat.tg_id, '⏰ В чате появился новый дроп!', DropIKB(0).open(drop.id), None) for drop in drops])
                    await self.layer.drops_to_open([d.id for d in drops])
                no_open_drops = await self.layer.get_drops(time=now, operator='>')
                print(f'📦 DropRunner send drop: {len(drops)}')
                chats = await self.layer.get_chats()
                chat_tasks = [self.create_drop(chat.tg_id) for chat in chats if chat.setting.receive_drops and chat.id not in [d.chat_id for d in no_open_drops]]
                new_drops = await self.asyncio.gather(*chat_tasks) if len(chat_tasks) > 0 else []
                print(f'📦 DropRunner create drop: {len(new_drops)}')
            except Exception as e:
                print('📦 DropRunner: ', e)
                return True
            finally:
                await self.asyncio.sleep(sleep_time)
 
    async def get_item(self, drop_id: int, sketch_id: int, quantity: int):
        item = await self.layer.get_item(drop_id, sketch_id, quantity)
        if item:
            await self.callback.answer(f'✅ Вы забрали {item.sketch.text}, теперь у вас {item.quantity} шт.')
        else:
            await self.callback.answer(f'❌ Вы успели забрать предмет')
        return await self.open_drop(drop_id)