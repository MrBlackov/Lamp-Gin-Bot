from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.stats import StatsIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.stats import TextHTML, StatsText
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from app.interlayer.stats import StatsLayer
from app.aio.cls.fsm.utils import StatsFSM

class StatsService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = StatsLayer(tg_id)
        self.text = StatsText
        self.state = StatsFSM(state)
        self.IKB = StatsIKB(tg_id)

    async def all_coins(self):
        stats = await self.layer.all()
        text = self.text(stats).all_coins
        return text
    
    async def menu(self):
        return
    
    async def tops(self):
        return '🏅 Выберите нужный топ', self.IKB.tops()

    async def topskills(self):
        skills = await self.layer.get_skills()
        return '💡 Выберите навык', self.IKB.topskills(skills, 'tops')

    async def topskill(self, skill_tag: str, values: int = 5):
        skills = (await self.layer.topskill(skill_tag))[:values]
        if len(skills) == 0:
            return '🏆 Персонажи пока не получили этот навык', self.IKB.back('topskills')
        return self.text.topskill(skill_tag, skills), self.IKB.topskill(skill_tag, 'topskills')
