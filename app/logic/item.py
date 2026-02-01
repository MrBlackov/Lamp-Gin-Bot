from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.metods.adds import add_item, add_item_sketch, ItemDB, ItemSketchDB
from app.db.metods.gets import get_item, get_item_for_id, get_char_for_id, get_items_for_inventory, get_item_sketch, get_item_sketchs
from app.db.metods.updates import update_quantity_item, update_item_sketch_for_id
from app.db.metods.deletes import delete_item_for_id, delete_item_sketch_for_id, delete_items_for_sketch_id
from app.db.metods.another import get_items_and_chars_for_sketch
from app.logged.botlog import log
from app.exeption.item import ThrowAwayQuantityLessOne, ThrowAwayQuantityMoreItemQuantity
from app.exeption.char import InventaryOverFlowing
from app.db.models.char import CharacterDB

class ItemSketchsLogic:
    async def create(self, item: ItemSketchValide) -> ItemSketchDB:
        log.info(f' User({item.creator_id}) created new item_sketch: {item.model_dump()}')
        return await add_item_sketch(data=item)
    
    async def get_sketchs(self):
        return await get_item_sketchs()
    
    async def update_sketch(self, item_id: int, new_data: dict):
        return await update_item_sketch_for_id(item_id, new_data)
    
    async def get_items_for_sketch(self, sketch_id: int) -> ItemSketchDB:
        return await get_items_and_chars_for_sketch(sketch_id=sketch_id)
    
    async def delete_sketch(self, sketch_id: int):
        return await delete_item_sketch_for_id(sketch_id)

class ItemsLogic:
    async def give(self, sketch_id: int, inventory_id: int, char_id: int, quantity: int = 1) -> ItemDB:
        item = await get_item(sketch_id, inventory_id)
        sketch = item.sketch
        char = await get_char_for_id(char_id)
        items = await get_items_for_inventory(inventory_id)
        max_size = char.exist.attibute_point.strength*1000
        size = 0
        for i in items:
            size += i.sketch.size*i.quantity

        if size+sketch.size*quantity > max_size:
            raise InventaryOverFlowing(f'This char({char_id}) inventary is full')

        log.info(f'Give item(sketch_id: {sketch_id}) for char(char_id: {char_id}), quantity: {quantity}')
        if item:
            return await update_quantity_item(item.id, item.quantity + quantity)
        return await add_item(data=ItemValide(inventory_id=inventory_id, sketch_id=sketch_id, quantity=quantity))
    
    @log.decor(arg=True)
    async def action(self, item: ItemDB, char: CharacterDB, action: str, quantity: int = 1):
        items = await get_items_for_inventory(char.exist.inventory.id)
        max_size = char.exist.attibute_point.strength*1000
        size = 0
        for i in items:
            if i.id == item.id:
                continue
            size += i.sketch.size*i.quantity
        quan = item.quantity
        if action == '+':
            quan += quantity
        elif action == '-':
            quan -= quantity
        else:
            raise

        if quan <= 0:
            return (False, None) if await delete_item_for_id(item.id) else (None, item)
   
        print(quan*item.sketch.size)
        print(max_size)
        if size+(quan*item.sketch.size) > max_size:
            raise InventaryOverFlowing(f'This char({char.id}) inventary is full')
        
        log.info(f'Action item(item_id: {item.id}) for user(char_id: {char.id}), quantity: {quantity}')            
        return True, await update_quantity_item(item.id, quan)


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

    async def delete_items(self, sketch_id: int) -> bool:
        return await delete_items_for_sketch_id(sketch_id)