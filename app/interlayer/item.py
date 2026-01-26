from app.validate.sketchs.item_sketchs import ItemSketchValide
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.db.metods.gets import get_user_for_tg_id, get_main_char_for_user_id, get_char_for_id


class ItemLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def get_char_info(self):
        self.user_id = await get_user_for_tg_id(self.tg_id)
        self.char_id = await get_main_char_for_user_id(self.user_id)
        self.char = await get_char_for_id(self.char_id)
        return self

    def data_to_valid(self, data: str):
        return ItemSketchValide(**data)

    async def create(self, item: ItemSketchValide):
        self = await self.get_char_info()
        new_sketch = await ItemSketchsLogic().create(item)
        new_item = await ItemsLogic().give(new_sketch.id, self.char.exist.inventory.id)
        return True
   

