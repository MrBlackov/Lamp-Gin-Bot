from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.db.metods.adds import add_item, add_item_sketch, ItemDB, ItemSketchDB, add_db_obj
from app.db.metods.gets import (get_item, 
                                get_item_for_id, 
                                get_char_for_id, 
                                get_items_for_location, 
                                get_items_for_inventory, 
                                get_item_sketch, 
                                get_item_sketchs)
from app.db.metods.updates import (update_quantity_item, 
                                   update_item_sketch_for_id, 
                                   update_quantity_items,
                                   update_look_location_item,
                                   update_item_throw_away,
                                   update_items_pick_up_for_ids)
from app.db.metods.deletes import delete_item_for_id, delete_item_sketch_for_id, delete_items_for_sketch_id, delete_items
from app.db.metods.another import get_items_and_chars_for_sketch
from app.logged.botlog import log
from app.exeption.item import ThrowAwayQuantityLessOne, ThrowAwayQuantityMoreItemQuantity, MaxDropLessMinDropError, ItemError
from app.exeption.char import InventaryOverFlowing, InventaryNoHaveError
from app.db.models.char import CharacterDB
from app.exeption.transfer import TransferNoHaventItemError

class ItemSketchsLogic:
    async def create(self, item: ItemSketchValide) -> ItemSketchDB:
        if item.max_drop < item.min_drop:
            raise MaxDropLessMinDropError(f'This item(name:{item.name}) to created, but max_drop < min_drop')
        log.info(f' User({item.creator_id}) created new item_sketch: {item.model_dump()}')
        item_dict = item.model_dump()
        item_dict['_emodzi'] = item_dict.pop('base_emodzi')
        return (await add_db_obj(data=[ItemSketchDB(**item_dict)]))[0]
    
    async def get_sketch(self, sketch_id: int):
        return await get_item_sketch(sketch_id)

    async def get_sketchs(self, is_hide: bool = False):
        return await get_item_sketchs(is_hide)
    
    async def update_sketch(self, item_id: int, new_data: dict):
        return await update_item_sketch_for_id(item_id, new_data)

    async def get_items_for_sketch(self, sketch_id: int) -> ItemSketchDB:
        return await get_items_and_chars_for_sketch(sketch_id=sketch_id)
    
    async def delete_sketch(self, sketch_id: int):
        return await delete_item_sketch_for_id(sketch_id)
    
    async def create_sketch_for_user(self, sketch_id: int):
        return await self.update_sketch(sketch_id, {'is_hide':False})
    
    async def delete_sketch_for_user(self, sketch_id: int):
        sketch = await get_item_sketch(sketch_id)
        await self.delete_sketch(sketch_id)
        return sketch


class ItemsLogic:
    async def give(self, sketch_id: int, inventory_id: int, char: CharacterDB, quantity: int = 1, size_except: bool = True, to_max_quantity: bool = False) -> ItemDB | None:
        try:
            item = await get_item(sketch_id, inventory_id)
            sketch = item.sketch if item else await get_item_sketch(sketch_id)
            items = await get_items_for_inventory(inventory_id)
            max_size = char.exist.attibute_point.skill_tags.get('inventory').level*1000
            size = 0
            for i in items:
                size += i.sketch.size*i.quantity
    
            if to_max_quantity:
                while size+sketch.size*quantity > max_size:
                    quantity -= 1
            
            if quantity == 0:
                raise InventaryOverFlowing(f'This char({char.id}) inventary is full')

            if size+sketch.size*quantity > max_size:
                raise InventaryOverFlowing(f'This char({char.id}) inventary is full')
    
            log.info(f'Give item(sketch_id: {sketch_id}) for char(char_id: {char.id}), quantity: {quantity}')
            if item:
                return await update_quantity_item(item.id, item.quantity + quantity)
            return await add_item(data=ItemValide(inventory_id=inventory_id, sketch_id=sketch_id, quantity=quantity))
        except InventaryOverFlowing as e:
            if size_except:
                raise 
            return None
        except Exception:
            raise

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
            raise ItemError(f'Action({action}) not + or -')

        if quan <= 0:
            return (False, None) if await delete_item_for_id(item.id) else (None, item)
   
        if size+(quan*item.sketch.size) > max_size and action == '+':
            raise InventaryOverFlowing(f'This char({char.id}) inventary is full')
        
        log.info(f'Action item(item_id: {item.id}) for user(char_id: {char.id}), quantity: {quantity}')            
        return True, await update_quantity_item(item.id, quan)

    def check_size_inventory(self, char: CharacterDB, inventory_items: list[ItemDB] | None, new_items: list[ItemDB], action: str):
        if new_items == None:
            return True

        if inventory_items == None:
            inventory_items = []
        max_size = char.exist.attibute_point.strength*1000
        for inv_item in inventory_items:
            max_size -= inv_item.quantity*inv_item.sketch.size
  
        if action == '+':   
            size = 0
            for item in new_items:
               size += item.quantity*item.sketch.size
    
            if size > max_size:
                raise InventaryOverFlowing(f'This char({char.id}) inventary is full')
        return True
    
    def check_size_inventory_for_item(self, char: CharacterDB, inventory_items: list[ItemDB] | None, new_item: ItemDB, action: str, quantity: int = 0):
        if inventory_items == None:
            inventory_items = []
        max_size = char.exist.attibute_point.strength*1000
        for inv_item in inventory_items:
            max_size -= inv_item.quantity*inv_item.sketch.size
  
        if action == '+':
            size = quantity*new_item.sketch.size
            if size > max_size:
                raise InventaryOverFlowing(f'This char({char.id}) inventary is full')
        return True
      
    def check_have_item(self, char: CharacterDB, item_id :int, quantity: int):
        item = char.exist.inventory.item_ids.get(item_id)
        if item.quantity < quantity:
            raise InventaryNoHaveError(f'This char(id={char.id}) not have quantity by item')
        return True

    @log.decor(arg=True)
    async def action_for_items(self, items: list[ItemDB], char: CharacterDB, action: str, quantity: int | None = None, is_pick_up: bool = False):
        inventory_items = await get_items_for_inventory(char.exist.inventory.id)
        
        if is_pick_up and quantity:
            self.check_size_inventory_for_item(char, inventory_items, items[0], action, quantity)
        else:
            self.check_size_inventory(char, inventory_items, items, action)

        inv_item_id = {i.sketch_id: i for i in inventory_items}
        new_item: list[ItemDB] = []
        delete_item: list[int] = []
        update_item: dict[int, int] = {}
        for item in (items or []):
            if is_pick_up:
                item_quantity = quantity
            else:
                item_quantity = item.quantity
            # determine sketch id robustly (support objects with sketch or sketch_id)
            inventory_item = inv_item_id.get(item.sketch_id)
            if action == '+':
                if inventory_item:
                    update_item[inventory_item.id] = inventory_item.quantity + item_quantity
                else:
                    new_item.append(ItemDB(sketch_id=item.sketch_id, 
                                               quantity=quantity, 
                                               inventory_id=char.exist.inventory.id, 
                                               nbt=item.nbt))
            elif action == '-':
                if inventory_item:
                    if inventory_item.quantity - item_quantity <= 0:
                        delete_item.append(inventory_item.id)
                    else:
                        update_item[inventory_item.id] = inventory_item.quantity - item_quantity
            
            if is_pick_up:
                if item.quantity - quantity > 0:
                    update_item[item.id] = item.quantity - quantity
                else:
                    delete_item.append(item.id)
                break

        await add_db_obj(data=new_item)
        await update_quantity_items(update_item)
        await delete_items(delete_item)
        return True

    async def throw_away(self, item_id: int | None = None, quantity: int = 1, location_id: int = 1, item: ItemDB | None = None) -> bool:
        if quantity < 1:
            raise ThrowAwayQuantityLessOne('User enter quantity < 1')
        item = await get_item_for_id(item_id) if item == None else item
        if item.quantity < quantity:
            raise ThrowAwayQuantityMoreItemQuantity('User enter quantity > item.quantity')
        elif item.quantity > 1 and item.quantity - quantity > 0:
            update = await update_quantity_item(item.id, item.quantity - quantity)
            if update:
                return await add_db_obj(data=[ItemDB(sketch_id=update.sketch_id, 
                                               quantity=quantity, 
                                               location_id=location_id, 
                                               nbt=update.nbt | {'is_pick_up':False})])
        return await update_item_throw_away(item.id, location_id)

    async def delete_items(self, sketch_id: int) -> bool:
        return await delete_items_for_sketch_id(sketch_id)
    
    async def delete_item(self, item_id: int) -> bool:
        return await delete_item_for_id(item_id)
    
    async def get_item_id(self, item_id: int) -> ItemDB | None:
        return await get_item_for_id(item_id)
    
    async def look_location_items(self, location_id: int, inventory_id: int) -> list[ItemDB]:
        items_no_pick_up, items_pick_up = await get_items_for_location(location_id)
        await update_items_pick_up_for_ids([i.id for i in items_pick_up if i.inventory_id == inventory_id])
        return items_no_pick_up

    async def look_location_item(self, item_id: int, inventory_id: int) -> ItemDB | None:
        item = await self.get_item_id(item_id)
        if item:
            if item.is_pick_up and item.inventory_id != inventory_id:
                return None
            return await update_look_location_item(item_id, inventory_id, True)

    async def throw_back(self, item_id: int, inventory_id: int): 
        item = await self.get_item_id(item_id)
        if item:
            return await update_look_location_item(item_id,inventory_id, False)

