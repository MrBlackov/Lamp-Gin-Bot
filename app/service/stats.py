from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.faq import FaqIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.stats import TextHTML, StatsText
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from app.interlayer.stats import StatsLayer


class StatsService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = StatsLayer(tg_id)
        self.text = StatsText

    async def all_coins(self):
        stats = await self.layer.all()
        text = self.text(stats).all_coins
        print(text)
        return text



