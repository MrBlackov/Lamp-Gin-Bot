from app.interlayer.base import BaseLayer
from app.logic.craft import CraftLogic
from app.logic.item import ItemSketchsLogic

class CraftLayer(BaseLayer):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.logic = CraftLogic()
        self.item_sketch = ItemSketchsLogic()

    async def get_crafts_for_no_hide(self):
        return await self.logic.get_crafts(no_hide=True)

    async def get_craft_for_id(self, craft_id: int):
        return await self.logic.get_craft(craft_id=craft_id)
