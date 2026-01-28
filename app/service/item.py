from app.service.base import BaseService
from app.interlayer.item import ItemLayer
from app.aio.inline_buttons.item import AddItemIKB
from aiogram.types import Document
from app.aio.config import bot
from app.service.utils import str_to_json
import json
from app.exeption.item import GiveItemQuantityLessOne, GiveItemNoEnterNameOrID, GiveItemNoInt

class ItemService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = AddItemIKB()
        self.layer = ItemLayer(tg_id)

    async def add_data_item(self, string: str | None = None, document: Document | None = None):
        if string:
            sketch = str_to_json(string)
        elif document:
            tgfile = await bot.get_file(document.file_id)
            await bot.download_file(tgfile.file_path, 'app/service/sketch.json')
            with open('app/service/sketch.json', 'w', encoding='utf-8') as file:
                line = file.read()
            sketch = json.loads(line)
        sketch = self.layer.data_to_valid(sketch)
        add_item = await self.layer.create(sketch)
        if add_item: 
            return 'Предмет создан, посмотреть /inventory'
        
    async def give(self, string: str):
        print(string)
        data = str_to_json(string)
        name = data.get('data')
        item_id: str = data.get('id')
        quantity: str = data.get('quan')
        if quantity == None:
            quantity = data.get('quantity', 1)  

        if name == None and item_id == None:
            raise GiveItemNoEnterNameOrID(f'This tg_user({self.tg_id}) dont enter id or name')
        if item_id.isalnum() == False:
            raise GiveItemNoInt(f'This tg_user({self.tg_id}) enter no int ID')
        if quantity and type(quantity) == str:         
            if quantity.isalnum() == False:
                raise GiveItemNoInt(f'This tg_user({self.tg_id}) enter no int quantity')

        if int(quantity) < 1:
            raise GiveItemQuantityLessOne(f'This tg_user({self.tg_id}) enter quantity < 1')

        if item_id:
            item = await self.layer.give(int(item_id), quantity=int(quantity))
        elif name:
            item = await self.layer.give(name=name, quantity=int(quantity))

        if item:
            return f'Выдан предмет({item.sketch.name}) в количестве {quantity} шт'
        




