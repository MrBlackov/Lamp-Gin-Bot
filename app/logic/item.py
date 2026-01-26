from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.metods.adds import add_item, add_item_sketch, ItemDB, ItemSketchDB
from app.db.metods.gets import get_item
from app.db.metods.updates import update_quantity_item
from app.logged.botlog import log

class ItemSketchsLogic:
    async def create(self, item: ItemSketchValide) -> ItemSketchDB:
        log.info(f'Created new item_sketch: {item.model_dump()}')
        return await add_item_sketch(data=item)

class ItemsLogic:
    async def give(self, sketch_id: int, inventory_id: int, quantity: int = 1) -> ItemDB:
        item = await get_item(sketch_id, inventory_id)
        log.info(f'Give item(sketch_id: {sketch_id}) for user(inventory_id: {inventory_id}), quantity: {quantity}')
        if item:
            return await update_quantity_item(item.id, item.quantity + quantity)
        return await add_item(data=ItemValide(inventory_id=inventory_id, sketch_id=sketch_id, quantity=quantity))