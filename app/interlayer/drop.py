from app.interlayer.base import BaseLayer
from app.logic.drop import DropLogic
from app.logic.item import ItemsLogic
from app.exeption.drop import DropEmptyError

class DropLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = DropLogic()
        self.item_logic = ItemsLogic()

    async def get_drop(self, chat_tg_id: int):
        return await self.logic.get_drop_for_chat(chat_tg_id)

    async def open_drop(self, drop_id: int):
        return await self.logic.open_drop(drop_id)
    
    async def create_drop(self, chat_tg_id: int, coins: int, is_random: bool = True):
        return await self.logic.create_drop(chat_tg_id, coins, is_random)

    async def get_drops(self, time, arg_name: str = 'open', operator: str = '<=', **kwargs):
        return await self.logic.get_drops(time=time, arg_name=arg_name, operator=operator, **kwargs)

    async def get_chats(self):
        return await self.logic.get_chats()
    
    async def get_item(self, drop_id: int, sketch_id: int, quantity: int):
        await self.get_char_info()
        drop = await self.logic.get_drop(drop_id)
        if drop == None:
            return None
        items = drop.items
        if (sketch_id, quantity) not in items:
            return False
        items.remove((sketch_id, quantity))
        await self.drop_redact_items(drop.id, [f'{id}:{q}' for id, q in items])
        return await self.item_logic.give(sketch_id, self.char.exist.inventory.id, self.char, quantity, to_max_quantity=True)
         
    async def drop_redact_items(self, drop_id: int, new_items: list[str]):
        return await self.logic.update_drops([drop_id], {'_items':new_items})
    
    async def drops_to_open(self, drop_ids: list[int]):
        return await self.logic.update_drops(drop_ids, {'is_open':True})
