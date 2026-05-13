from app.interlayer.base import BaseLayer
from app.logic.stats import StatsLogic
class StatsLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = StatsLogic()

    async def all(self):
        return await self.logic.get_all()
    
    async def get_skills(self):
        return await self.logic.get_skills()

    async def topskill(self, skill_tag: str):
        return await self.logic.topskill(skill_tag)