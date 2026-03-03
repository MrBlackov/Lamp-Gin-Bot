from app.interlayer.base import BaseLayer
from app.logic.craft import CraftLogic, ItemDB
from app.logic.item import ItemSketchsLogic

class CraftLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = CraftLogic()
        self.item_sketch = ItemSketchsLogic()

    async def get_crafts_for_no_hide(self):
        return await self.logic.get_crafts(is_hide=False)

    async def get_craft_for_id(self, craft_id: int):
        return await self.logic.get_craft(craft_id=craft_id)

    async def add_craft(self, 
                        ingredients: list[ItemDB] | None = None, 
                        tools: list[ItemDB] | None = None, 
                        results: list[ItemDB] | None = None, 
                        time: int = 0):
        await self.get_char_info()
        return await self.logic.new_craft(user_id=self.user.id, ingredients=ingredients, tools=tools, results=results, time=time)
    
    async def send_craft(self, 
                        ingredients: list[ItemDB] | None = None, 
                        tools: list[ItemDB] | None = None, 
                        results: list[ItemDB] | None = None, 
                        time: int = 0):
        await self.get_char_info()
        return await self.logic.new_craft(user_id=self.user.id, ingredients=ingredients, tools=tools, results=results, time=time, is_hide=True)
