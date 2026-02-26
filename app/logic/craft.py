from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_craft_for_id, get_crafts
from app.db.metods.unique import get_crafts_for_item_id
from app.logged.botlog import log
from app.db.models.item import CraftDB

class CraftLogic:
    async def get_craft(self, craft_id: int) -> CraftDB | None:
        return await get_craft_for_id(craft_id=craft_id)
    
    async def get_crafts(self, no_hide: bool | None = True) -> list[CraftDB] | None:
        return await get_crafts(no_hide=no_hide)

