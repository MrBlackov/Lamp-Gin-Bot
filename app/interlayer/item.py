from app.validate.sketchs.item_sketchs import ItemSketchValide
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.db.metods.gets import get_user_for_tg_id, get_main_char_for_user_id, get_char_for_id, get_item_for_name, get_item_sketch
from app.exeption.item import ItemError
from app.db.models.item import ItemDB
from app.db.models.char import CharacterDB
from app.exeption.item import SizeNotIntItemSketchError, NameNoValideError, EmodziNoValideError, NoFindItemSketchForID


class ItemLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = ItemsLogic()
        self.sketch_logic = ItemSketchsLogic()

    async def get_char_info(self):
        self.user_id = await get_user_for_tg_id(self.tg_id)
        self.char_id = await get_main_char_for_user_id(self.user_id)
        self.char = await get_char_for_id(self.char_id)
        return self



    async def create(self, item: dict):
        self = await self.get_char_info()
        new_sketch = await self.sketch_logic.create(ItemSketchValide(**item, creator_id=self.user_id))
        new_item = await self.logic.give(new_sketch.id, self.char.exist.inventory.id, self.char.id, )
        return True



    async def give(self, sketch_id: int | None = None, name: str | None = None, quantity: int = 1):
        self = await self.get_char_info()
        if sketch_id == None and name:
            item0 = await get_item_for_name(name)
            item = await self.logic.give(item0.id, self.char.exist.inventory.id, self.char.id, quantity)
        elif sketch_id: 
            item = await self.logic.give(sketch_id, self.char.exist.inventory.id, self.char.id, quantity)
        else:
            raise ItemError('To give, but not enter sketcth_id or sketch_name')
        return item

    async def action(self, item: ItemDB, char: CharacterDB, action: str, quantity: int = 1):
        return await self.logic.action(item, char, action, quantity)

    async def get_item_sketchs(self):
        return await self.sketch_logic.get_sketchs()
    


    async def sell(self, item_id: int, buyer_char_id: int, price: int | None = None, cost: int | None = None, quantity: int = 1):
        pass

    async def transfer(self, my_item_id: int, seller_char_id: int, get_char_id: int, my_quantity: int = 1, get_quantity: int = 1):
        pass   


   
    async def get_item_sketch(self, item_id: int):
        data = await get_item_sketch(item_id)
        if data == None:
            raise NoFindItemSketchForID(f'This user(tg_id={self.tg_id}) enter item_sketch_id, but dont find item_sketch')
        return data
    
    def change_data_valid(self, what_change: str, new_data: str):
        if what_change == 'name':
            if len(new_data) > 30:
                raise NameNoValideError(f'This user(tg_id={self.tg_id}) enter name and len(name) > 30')
        elif what_change == 'emodzi':
            if len(new_data) > 1:
                raise EmodziNoValideError(f'This user(tg_id={self.tg_id}) enter emodzi and len(emodzi) > 1')
        elif what_change == 'size':
            if new_data.isdigit() == False:
                raise SizeNotIntItemSketchError(f'This user(tg_id={self.tg_id}) enter size, but size no int')
            return int(new_data)
        return new_data

    async def get_items_for_sketchs(self, sketch_id: int) -> dict[CharacterDB, ItemDB]:
        sketch =  await self.sketch_logic.get_items_for_sketch(sketch_id)
        datas = {}
        for item in sketch.items:
            char = item.inventory.exist.char
            datas[char] = item
        return datas

    async def change_sketch(self, sketch_id: int, new_data: dict):
        return await self.sketch_logic.update_sketch(sketch_id, new_data)

    async def delete_sketch(self, sketch_id: int) -> bool:
        return await self.sketch_logic.delete_sketch(sketch_id)

    async def delete_items(self, sketch_id: int) -> bool:
        return await self.logic.delete_items(sketch_id)
  