from app.service.base import BaseService
from app.interlayer.item import ItemLayer
from app.aio.inline_buttons.item import AddItemIKB
from aiogram.types import Document
from app.aio.config import bot
from app.service.utils import str_to_json
import json


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

        




