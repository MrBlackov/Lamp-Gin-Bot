from app.interlayer.base import BaseLayer
from app.logic.stats import StatsLogic

class StatsLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = StatsLogic()

    async def all(self):
        return await self.logic.get_all()