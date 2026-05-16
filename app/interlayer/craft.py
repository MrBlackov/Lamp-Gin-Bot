from app.interlayer.base import BaseLayer
from app.logic.craft import CraftLogic, ItemDB
from app.logic.item import ItemSketchsLogic, ItemsLogic
from app.db.models.char import CharacterDB
from app.db.metods.gets import get_items_for_inventory
from app.exeption.craft import CraftNoHaventItemError, CraftNoHaventToolError

class CraftLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = CraftLogic()
        self.item_sketch = ItemSketchsLogic()
        self.item = ItemsLogic()

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
        return await self.logic.new_craft(user_id=self.user.id, ingredients=ingredients, tools=tools, results=results, time=time), self.user
    
    async def send_craft(self, 
                        ingredients: list[ItemDB] | None = None, 
                        tools: list[ItemDB] | None = None, 
                        results: list[ItemDB] | None = None, 
                        is_hide: bool = False,
                        time: int = 0):
        await self.get_char_info()
        return await self.logic.new_craft(user_id=self.user.id, ingredients=ingredients, tools=tools, results=results, time=time, is_hide=is_hide, is_create=False), self.user

    async def accert_new_craft(self, craft_id: int, to_create: bool):
        await self.get_char_info()
        result1, result2 =  await self.logic.accert_new_craft(craft_id, to_create)
        return result1, result2, self.user

    async def use_craft(self, craft_id: int, quantity: int):
        await self.get_char_info()
        await self.checking_freedom()
        craft = await self.logic.get_craft(craft_id=craft_id)
        await self.check_inventory(self.char, craft.ingredients, quantity)
        await self.check_inventory(self.char, craft.tools, is_tools=True)
        await self.logic.action_for_items(craft.ingredients, self.char, '-', quantity)
        await self.logic.action_for_items(craft.results, self.char, '+', quantity)
        return True

    async def check_inventory(self, char: CharacterDB, items: list[ItemDB] | None, craft_quantity: int = 1, is_tools: bool = False):
        inventory = await get_items_for_inventory(char.exist.inventory.id)
        inventory_items_id = {i.sketch.id: i for i in inventory}
        for item in items:
            if item.sketch.id not in inventory_items_id or inventory_items_id[item.sketch.id].quantity < item.quantity * craft_quantity:
                if is_tools:
                    raise CraftNoHaventToolError(f'This char(id={char.id}) has not enough item for transfers')
                raise CraftNoHaventItemError(f'This char(id={char.id}) has not enough item for transfers')
        return True

        
