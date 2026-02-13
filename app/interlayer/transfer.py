from app.logic.char import CharLogic
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.logic.transfer import TransferLogic
from app.interlayer.item import ItemLayer
from app.db.models.char import CharacterDB
from app.db.metods.gets import get_user_for_tg_id, get_user_for_id, get_main_char_for_user_id, get_char_for_id, get_item_for_name, get_item_sketch

class TransferLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.char = CharLogic(tg_id)
        self.item = ItemsLogic()
        self.item_sketch = ItemSketchsLogic()
        self.transfer = TransferLogic()

    async def get_char_info(self):
        self.user_id = await get_user_for_tg_id(self.tg_id)
        self.char_id = await get_main_char_for_user_id(self.user_id)
        self.char_info = await get_char_for_id(self.char_id)
        return self

    async def locator(self):
        await self.get_char_info()
        chars = await self.char.get_all_chars()
        return [char for char in chars if char.id != self.char_id]

    async def newtrade(self, 
                       char1: CharacterDB, 
                       char2: CharacterDB,
                       items1: list,
                       items2: list) -> int:
        trade = await self.transfer.new_transfer(char1.id, char2.id, items1, items2)
        user = await get_user_for_id(char2.user_id)
        return user.tg_id 