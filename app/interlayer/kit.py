from app.db.metods.gets import get_user_for_tg_id, get_main_char_for_user_id, get_char_for_id, get_user_for_id
from app.logic.kit import KitLogic, KitDB, KitSketchDB
from app.logic.item import ItemSketchsLogic

class KitLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = KitLogic()
        self.item_logic = ItemSketchsLogic()

    @property
    def kit_start(self):
        return self.logic.is_get_kit('start')

    async def get_char_info(self, user_id: int | None = None):
        if user_id:
            self.user = await get_user_for_id(user_id)
        else:
            self.user = await get_user_for_tg_id(self.tg_id, True)
        self.char_id = await get_main_char_for_user_id(self.user.id)
        self.char = await get_char_for_id(self.char_id)
        return self

    async def my_kits(self):
        self = await self.get_char_info()
        return await self.logic.get_kits_for_inventory(self.char.exist.inventory.id), await self.logic.get_kits_no_hide() 

    async def get_kit_for_code(self, code: str):
        return await self.logic.is_get_kit(code)

    async def kit_items(self, kit: KitSketchDB):
        if kit.all_item_skeths:
            return await self.item_logic.get_sketchs()
        if kit.item_skeths:
            return await self.logic.get_item_sketch_for_kit(kit.item_skeths)







