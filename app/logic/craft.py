from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_craft_for_id, get_crafts
from app.db.metods.unique import get_crafts_for_item_id
from app.db.metods.updates import update_craft_items, update_item_on_craft_id
from app.logged.botlog import log
from app.db.models.item import CraftDB, ItemDB

class CraftLogic:
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

