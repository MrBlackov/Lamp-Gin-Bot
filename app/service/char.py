from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import AddCharIKB, InfoCharIKB, InventoryIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.validate.api.characters import CharSketchInfo
from app.validate.api.query import CreateCharSkecth
from app.aio.msg.char import SketchInfoText, CharInfoText, InventoryItemsText
from app.aio.msg.utils import TextHTML
import random
from app.service.base import BaseService 
from app.interlayer.char import CreateCharacterLayer, InfoCharacterLayer, InventoryCharacterLayer
from app.aio.cls.fsm.char import InventoryState

class AddCharacterService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = AddCharIKB()

    def chouse_gender(self, to_change: bool = False):
        return self.IKB.chouse_gender(to_change)
    
    async def to_get_sketchs(self, gender: Gender, to_changes: bool = False):
        if to_changes == False:
            print(gender)
            api_data = CreateCharacterLayer.get_sketchs(gender)
            logs.debug(f'Class Character give GetSketchs({api_data})')
            await self.state.update_data(
                first_names=api_data.first_names, 
                last_names=api_data.last_names, 
                sketchs=api_data.sketchs, 
                gender=gender,
                free_sketchs_quantity=len(api_data.sketchs)
                )
        return self.IKB.chouse_regim_name()
    
    async def to_sketchs(self, first_names: bool = True):
        names: list[str] = await self.state.get_value('first_names' if first_names else 'last_names')
        sketchs: list = await self.state.get_value('sketchs')
        logs.debug(f'Class Character give GetSketchs({names, sketchs})')
        return self.IKB.chouse_regim_name(first_names)  
    
    async def to_random_name(self, first_names: bool = True):
        datas: list[str] = await self.state.get_value('first_names' if first_names else 'last_names')
        rnd_name = random.choice(datas)
        return self.IKB.get_rnd_name(rnd_name, first_names), rnd_name
    
    async def to_query_names_to_pages(self, query_value: str | None = None, values_in_page: str = 10):
        first_names: bool = await self.state.get_value('is_first_name')
        datas: list[str] = await self.state.get_value('first_names' if first_names else 'last_names', [])
        names = []
        if query_value:
            for data in datas:
                if query_value in data:
                    names.append(data)
        else:
            names = datas
        if len(names) > 0:
            name_pages = [tuple(names[i:i+values_in_page]) for i in range(0, len(names), values_in_page)]
            await self.state.update_data(name_pages=name_pages)
            return self.IKB.get_pages_names(list(name_pages[0]), 0, len(name_pages), first_names), f'Держите список, Страница: 0/{len(name_pages)}'
        else: 
            return self.IKB.query_back(first_names), 'Ничего не найдено'
    


    async def get_name_pages(self, page: int):
        first_names: bool = await self.state.get_value('is_first_name')
        pages: list[tuple[str]] = await self.state.get_value('name_pages')
        return self.IKB.get_pages_names(list(pages[page]), page, len(pages), first_names), f'Держите список, Страница: {page}/{len(pages)}'
 
    async def to_chouse_sketchs(self, sketch_id: int = 0, another: bool = False):
        sketchs: list[CharSketchInfo] = await self.state.get_value('sketchs')
        if another:
            sketch_id += 1
        return self.IKB.get_sketchs(sketch_id, len(sketchs)), SketchInfoText(sketchs[sketch_id]).text
     
    async def to_descript(self, sketch_id: int):
        print(sketch_id)
        last_name: str = await self.state.get_value('last_name')
        first_name: str = await self.state.get_value('first_name')
        sketchs: list[CharSketchInfo] = await self.state.get_value('sketchs')
        await self.state.update_data(sketch=sketchs[sketch_id])
        return  self.IKB.descript(), 'Описание?'

    async def get_info(self, descript: str | None = None):
        datas: dict = await self.state.get_data()
        first_name = datas['first_name']
        last_name = datas.get('last_name')
        sketch = datas['sketch']
        description = descript if descript else datas.get('description')

        self.char = CreateCharSkecth(
            first_name=first_name,
            last_name=last_name,
            sketch=sketch,
            description=description
        )
        return self

    @property
    def info_to_str(self):
        text = [f'🪪 {self.char.full_name}', f'\n{TextHTML(SketchInfoText(self.char.sketch).to_text(True)).blockquote()}']
        if self.char.description: text.append(f'\n{TextHTML(TextHTML(self.char.description).blockquote(True)).unescape}')
        return ''.join(text)
    
    async def markup_to_info(self):
        gender = await self.state.get_value('gender')
        return self.IKB.to_finish(gender)
 
    async def create(self, descript: str | None = None):
        char = await self.get_info(descript)
        api_data = await CreateCharacterLayer().add_char(self.tg_id, char.char)
        await self.state.clear()
        return True

class InfoCharacterService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = InfoCharIKB()

    async def get_chars(self):
        datas = await InfoCharacterLayer(self.tg_id).get_chars()
        if datas.no_chars:
            return None, '😕 У вас нет персонажей, создать - /newchar'
        chars = {}
        data = datas.chars
        for d in data:
            chars[d.id] = d
        await self.state.update_data(chars=chars, main_id=datas.main_id)
        chars = {char.id:char.exist.full_name for char in data}
        return self.IKB.get_list(datas.main_id, chars), '🪪 Ваши персонажи'

    async def get_char(self, char_id: int):
        data: dict = await self.state.get_value('chars')
        main_id: int = await self.state.get_value('main_id')
        char = data[char_id]
        return self.IKB.chouse_main_char(char_id, True if char_id == main_id else False), CharInfoText(char).text
    
    async def char_to_main(self, char_id: int):
        datas = await InfoCharacterLayer(self.tg_id).char_to_main(char_id)
        chars = {}
        data = datas.chars
        for d in data:
            chars[d.id] = d
        await self.state.update_data(chars=chars, main_id=datas.main_id)
        chars = {char.id:char.exist.full_name for char in data}
        return self.IKB.get_list(datas.main_id, chars), '🪪 Ваши персонажи'

class InventoryService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = InventoryIKB()

    async def inventory(self):
        inventory = await InventoryCharacterLayer(self.tg_id).inventory()
        items = {}
        if inventory.items:
            for item in inventory.items:
                items |= {item.id: item}
            await self.state.update_data(items=items)
            return InventoryItemsText.inventory(inventory.size/1000, inventory.max_size), self.IKB.items(items)
        return InventoryItemsText.no_items(), None
        

    async def get_item_info(self, item_id: int):
        items = await self.state.get_value('items')
        await self.state.update_data(item=item_id)
        if items:
            return InventoryItemsText.item(items[item_id]), self.IKB.throw('inventory')

    async def to_throw(self):
        await self.state.set_state(InventoryState.throw_quantity)
        return InventoryItemsText.throw(), self.IKB.back('item')

    async def throw_away(self, item_id: int, quantity: int):
        throw = await InventoryCharacterLayer(self.tg_id).throw_away(item_id, quantity)
        if throw: return await self.inventory()
        raise

class Character:
    def __init__(self, tg_id: int, state: FSMContext | None = None):
        self.tg_id = tg_id
        self.state = state
        self.to_create = AddCharacterService(tg_id, state)
        self.info = InfoCharacterService(tg_id, state)
        self.inventory = InventoryService(tg_id, state)
        