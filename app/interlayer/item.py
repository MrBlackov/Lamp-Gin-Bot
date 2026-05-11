from app.validate.sketchs.item_sketchs import ItemSketchValide
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.db.metods.gets import get_user_for_tg_id, get_item_sketch_for_tag, get_main_char_for_user_id, get_char_for_id, get_item_for_name, get_item_sketch, get_user_for_id
from app.exeption.item import ItemError
from app.db.models.item import ItemDB
from app.db.models.char import CharacterDB
from app.exeption.item import SizeNotIntItemSketchError, TagValideError, NBTValiteError, RariryValideError, NameNoValideError, EmodziNoValideError, NoFindItemSketchForID, ItemNoHideCreatedError
from app.exeption.char import NoHaveMainChar
from app.interlayer.base import BaseLayer
import json

class ItemLayer(BaseLayer):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = ItemsLogic()
        self.sketch_logic = ItemSketchsLogic()

    async def create(self, item: dict, user_id: int | None = None):
        self = await self.get_char_info(user_id)
        if self.char == None:
            raise NoHaveMainChar(f'This user(tg_id:{self.tg_id}) hanst main char')
        item.pop('creator_id')
        new_sketch = await self.sketch_logic.create(ItemSketchValide(**item, creator_id=self.user.id))
        is_hide = item.get('is_hide')
        if is_hide:
            return self.user, new_sketch
        new_item = await self.logic.give(new_sketch.id, self.char.exist.inventory.id, self.char, size_except=False)
        if new_item:
            return self.user, new_item.sketch
        return self.user, new_sketch

    async def give(self, sketch_id: int | None = None, name: str | None = None, quantity: int = 1, user_id: int | None = None, size_except: bool = True):
        self = await self.get_char_info(user_id)
        if self.char == None:
            raise NoHaveMainChar(f'This user(tg_id:{self.tg_id}) hanst main char')
        if sketch_id == None and name:
            item0 = await get_item_for_name(name)
            item = await self.logic.give(item0.id, self.char.exist.inventory.id, self.char, quantity, size_except)
        elif sketch_id: 
            item = await self.logic.give(sketch_id, self.char.exist.inventory.id, self.char, quantity, size_except)
        else:
            raise ItemError('To give, but not enter sketcth_id or sketch_name')
        return item

    async def action(self, item: ItemDB, char: CharacterDB, action: str, quantity: int = 1):
        return await self.logic.action(item, char, action, quantity)

    async def get_item_sketchs(self, is_hide: bool = False):
        return await self.sketch_logic.get_sketchs(is_hide)
    

    async def get_item_sketch(self, item_id: int):
        data = await get_item_sketch(item_id)
        if data == None:
            raise NoFindItemSketchForID(f'This user(tg_id={self.tg_id}) enter item_sketch_id, but dont find item_sketch')
        return data
    
    async def change_data_valid(self, what_change: str, new_data: str):
        match what_change:
            case 'name':
                if len(new_data) > 30:
                    raise NameNoValideError(f'This user(tg_id={self.tg_id}) enter name and len(name) > 30')
            case '_emodzi':
                if len(new_data) > 1:
                    raise EmodziNoValideError(f'This user(tg_id={self.tg_id}) enter emodzi and len(emodzi) > 1')
            case  'size' | 'min_drop' | 'max_drop':
                if new_data.isdigit() == False:
                    raise SizeNotIntItemSketchError(f'This user(tg_id={self.tg_id}) enter size, but size no int')
                return int(new_data)
            case  'rarity':
                try:
                    rarity = float(new_data)
                except (ValueError, TypeError):
                    raise RariryValideError('Rarity must be a float')
                if not( 0 <= rarity <= 1):
                    raise RariryValideError('Rarity must be between 0 and 1')
                return rarity
            case  'nbt':
                try:
                    return json.loads(new_data.replace("'", '"').replace('True', 'true').replace('False', 'false'))
                except:
                    raise NBTValiteError('NBT must be a dict')
            case 'tag':
                sketch = await get_item_sketch_for_tag(new_data)
                if sketch:
                    raise TagValideError(f'This user(tg_id={self.tg_id}) enter tag and this tag already exist')
        return new_data

    async def get_items_for_sketchs(self, sketch_id: int) -> dict[CharacterDB, ItemDB]:
        sketch =  await self.sketch_logic.get_items_for_sketch(sketch_id)
        datas = {}
        for item in sketch.items:
            if item.inventory_id:
                char = item.inventory.exist.char
                datas[char] = item
        return datas

    async def change_sketch(self, sketch_id: int, new_data: dict):
        return await self.sketch_logic.update_sketch(sketch_id, new_data)

    async def delete_sketch(self, sketch_id: int) -> bool:
        return await self.sketch_logic.delete_sketch(sketch_id)

    async def delete_items(self, sketch_id: int) -> bool:
        return await self.logic.delete_items(sketch_id)

 
    async def create_before_moder(self, sketch_id: int, to_create: bool):
        await self.get_char_info()
        sketch = await self.sketch_logic.get_sketch(sketch_id)
        if to_create and sketch.is_hide:
            sketch = await self.sketch_logic.create_sketch_for_user(sketch_id)
            create = True
        elif sketch.is_hide:
            create = False
        else:
            raise ItemNoHideCreatedError(f'ItemSketch(id:{sketch_id}) created, dont to be create')
        self = await self.get_char_info(sketch.creator_id)
        await self.give(sketch_id, user_id=self.user.id, size_except=False)
        return self.user, create, sketch




