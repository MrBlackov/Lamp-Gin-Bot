from app.validate.sketchs.item_sketchs import ItemSketchValide
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.db.metods.gets import get_user_for_tg_id, get_main_char_for_user_id, get_char_for_id, get_item_for_name
from app.exeption.item import ItemError

class ItemLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = ItemsLogic()
        self.sketch_logic = ItemSketchsLogic()

    async def get_char_info(self):
        self.user_id = await get_user_for_tg_id(self.tg_id)
        self.char_id = await get_main_char_for_user_id(self.user_id)
        self.char = await get_char_for_id(self.char_id)
        return self

    def data_to_valid(self, data: str):
        return ItemSketchValide(**data)

    async def create(self, item: ItemSketchValide):
        self = await self.get_char_info()
        new_sketch = await self.sketch_logic.create(item)
        new_item = await self.logic.give(new_sketch.id, self.char.exist.inventory.id, self.char.id)
        return True
    
    async def give(self, sketch_id: int | None = None, name: str | None = None, quantity: int = 1):
        self = await self.get_char_info()
        if sketch_id == None and name:
            item0 = await get_item_for_name(name)
            item = await self.logic.give(item0.id, self.char.exist.inventory.id, self.char.id, quantity)
        elif sketch_id: 
            item = await self.logic.give(sketch_id, self.char.exist.inventory.id, self.char.id, quantity)
        else:
            raise ItemError('To give, but not enter sketcth_id or sketch_name')
        return item
   

