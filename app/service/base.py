from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import BotIKB
from app.logged.botlog import logs
from app.aio.config import admins, bot, newspaper_id
from app.aio.cls.fsm.utils import FSMUtils
from aiogram.types import Message
import asyncio

NOT_NEW_STATE = object()

class BaseService:
    def __init__(self, tg_id: int, state: FSMContext | None = None, message: Message | None = None, **kwargs):
        self.tg_id = tg_id
        self.state: FSMUtils = FSMUtils(state)
        self.IKB = BotIKB(tg_id)
        self.newspaper_id = newspaper_id
        self.admins = admins
        self.bot = bot
        self.message = message

    async def get_channel_info(self):
        channel = await self.bot.get_chat(self.newspaper_id)
        return channel
    
    async def get_chat_member(self, tg_id: int | None = None):
        if tg_id:
            return await bot.get_chat_member(self.newspaper_id, tg_id)
        return await bot.get_chat_member(self.newspaper_id, self.tg_id)

    async def another(self, tg_id: int, state: FSMContext | None = NOT_NEW_STATE):
        self.tg_id = tg_id
        if state != NOT_NEW_STATE:
            self.state = state
        return self

    async def text_boardcast(self, tg_ids: list[int], text: str, delay: int = 20):
        k = 0
        for tg_id in tg_ids:
            k += 1
            await self.bot.send_message(tg_id, text)
            if k%delay == 0:
                await asyncio.sleep(2)
        return True




