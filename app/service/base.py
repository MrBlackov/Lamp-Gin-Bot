from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import BotIKB
from app.logged.botlog import logs
from app.aio.config import admins, bot, newspaper_id

class BaseService:
    def __init__(self, tg_id: int, state: FSMContext | None = None):
        self.tg_id = tg_id
        self.state = state
        self.IKB = BotIKB()
        self.newspaper_id = newspaper_id
        self.admins = admins
        self.bot = bot

    async def get_channel_info(self):
        channel = await self.bot.get_chat(self.newspaper_id)
        return channel
    
    async def get_chat_member(self, tg_id: int | None = None):
        if tg_id:
            return await bot.get_chat_member(self.newspaper_id, tg_id)
        return await bot.get_chat_member(self.newspaper_id, self.tg_id)

    


