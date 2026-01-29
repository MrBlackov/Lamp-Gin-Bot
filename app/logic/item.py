from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.metods.adds import add_item, add_item_sketch, ItemDB, ItemSketchDB
from app.db.metods.gets import get_item, get_item_for_id, get_char_for_id, get_items_for_inventory, get_item_sketch, get_item_sketchs
from app.db.metods.updates import update_quantity_item
from app.db.metods.deletes import delete_item_for_id
from app.logged.botlog import log
from app.exeption.item import ThrowAwayQuantityLessOne, ThrowAwayQuantityMoreItemQuantity
from app.exeption.char import InventaryOverFlowing

class ItemSketchsLogic:
    async def create(self, item: ItemSketchValide) -> ItemSketchDB:
        log.info(f'Created new item_sketch: {item.model_dump()}')
        return await add_item_sketch(data=item)
    
    async def get_sketchs(self):
        return await get_item_sketchs()

class ItemsLogic:
    async def give(self, sketch_id: int, inventory_id: int, char_id: int, quantity: int = 1) -> ItemDB:
        item = await get_item(sketch_id, inventory_id)
        char = await get_char_for_id(char_id)
        items = await get_items_for_inventory(inventory_id)
        sketch = await get_item_sketch(sketch_id)
        max_size = char.exist.attibute_point.strength*1000
        size = 0
        for item in items:
            size += item.sketch.size*item.quantity

        if size+sketch.size*quantity > max_size:
            raise InventaryOverFlowing(f'This char({char_id}) inventary is full')

        log.info(f'Give item(sketch_id: {sketch_id}) for user(inventory_id: {inventory_id}), quantity: {quantity}')
        if item:
            return await update_quantity_item(item.id, item.quantity + quantity)
        return await add_item(data=ItemValide(inventory_id=inventory_id, sketch_id=sketch_id, quantity=quantity))
    
    async def throw_away(self, item_id: int, quantity: int = 1) -> bool:
        if quantity < 1:
            raise ThrowAwayQuantityLessOne('User enter quantity < 1')
        item = await get_item_for_id(item_id)
        if item.quantity < quantity:
            raise ThrowAwayQuantityMoreItemQuantity('User enter quantity > item.quantity')
        elif item.quantity > 1 and item.quantity - quantity > 0:
            update = await update_quantity_item(item_id, item.quantity - quantity)
            if update:
                return True
            return False
        return await delete_item_for_id(item_id)
