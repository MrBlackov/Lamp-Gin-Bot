from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_craft_for_id, get_crafts, get_items_for_inventory
from app.db.metods.unique import get_crafts_for_item_id
from app.db.metods.updates import update_craft_items, update_item_on_craft_id, CharacterDB, update_quantity_items
from app.db.metods.deletes import delete_items
from app.logged.botlog import log
from app.db.models.item import CraftDB, ItemDB
from app.logic.item import ItemsLogic
from app.exeption.craft import CraftNoHaventItemError

class CraftLogic:
    def __init__(self):
        self.item_logic = ItemsLogic()

    async def new_craft(self, 
                        user_id: int,
                        ingredients: list[ItemDB] | None = None, 
                        tools: list[ItemDB] | None = None, 
                        results: list[ItemDB] | None = None, 
                        time: int = 0,
                        is_hide: bool = False) -> CraftDB:
        await add_db_obj(data=ingredients + tools + results)
        ingredients = ingredients or []
        tools = tools or []
        results = results or []
        items = ingredients + tools + results
        craft = CraftDB(creator_id=user_id, 
                        ingredient_ids=[i.id for i in ingredients], 
                        result_ids=[i.id for i in results], 
                        tool_ids=[i.id for i in tools], time=time, 
                        is_hide=is_hide)
        await add_db_obj(data=[craft])
        await update_item_on_craft_id(craft.id, [i.id for i in items])
        return craft


    async def get_craft(self, craft_id: int):
        return await get_craft_for_id(craft_id=craft_id)
    
    async def get_crafts(self, is_hide: bool | None = True) -> list[CraftDB] | None:
        return await get_crafts(is_hide=is_hide)

    @log.decor(arg=True)
    async def action_for_items(self, items: list[ItemDB], char: CharacterDB, action: str, craft_quantity: int = 1):
        inventory_items = await get_items_for_inventory(char.exist.inventory.id)

        self.item_logic.check_size_inventory(char, inventory_items, items, action)

        inv_item_id = {i.sketch_id: i for i in inventory_items}
        new_item: list[ItemDB] = []
        delete_item: list[int] = []
        update_item: dict[int, int] = {}
        for item in (items or []):
            # determine sketch id robustly (support objects with sketch or sketch_id)
            inventory_item = inv_item_id.get(item.sketch_id)
            if action == '+':
                if inventory_item:
                    update_item[inventory_item.id] = inventory_item.quantity + item.quantity*craft_quantity
                else:
                    new_item.append(ItemDB(inventory_id=char.exist.inventory.id, sketch_id=item.sketch_id, quantity=item.quantity*craft_quantity))
            elif action == '-':
                if inventory_item:
                    if inventory_item.quantity - item.quantity*craft_quantity <= 0:
                        delete_item.append(inventory_item.id)
                    else:
                        update_item[inventory_item.id] = inventory_item.quantity - item.quantity*craft_quantity
                else:
                    raise CraftNoHaventItemError(f'This char(id={char.id}) has not enough item for transfers')

        await add_db_obj(data=new_item)
        await update_quantity_items(update_item)
        await delete_items(delete_item)
        return True
   