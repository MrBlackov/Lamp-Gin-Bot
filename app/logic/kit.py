from app.db.metods.adds import KitDB, KitSketchDB, add_kit_dict, add_kit, add_kit_sketch, add_db_obj
from app.db.metods.gets import get_kit_for_id, get_kit_sketch_for_id, get_kit_for_sketch_id, get_item_sketchs, get_kit_sketch_for_code, get_kits, get_kit_sketch_for_hide


class KitLogic:
    async def new_kit(self, inventory_id: int, sketch_id: int):
        return await add_db_obj(data=[KitDB(inventory_id=inventory_id, sketch_id=sketch_id)])

    async def is_get_kit(self, code: str):
        return await get_kit_sketch_for_code(code)

    async def get_kits_for_inventory(self, inventory_id: int) -> list[KitDB] | None:
        return await get_kits(inventory_id=inventory_id)

    async def get_kits_no_hide(self):
        return await get_kit_sketch_for_hide(False)
   
    async def get_item_sketch_for_kit(self, items_id: list[int]):
        sketchs =  await get_item_sketchs()
        return [sketch for sketch in sketchs for item_id in items_id if sketch.id == item_id]