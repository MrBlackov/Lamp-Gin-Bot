from app.service.base import BaseService
from app.interlayer.item import ItemLayer
from aiogram.types import Document
from app.aio.config import bot

class ItemService(BaseService):
    async def newitem(self, string: str | None = None, document: Document | None = None):
        if string:
            sketch = string
        elif document:
            tgfile = await bot.get_file(document.file_id)
            await bot.download_file(tgfile.file_path, 'app\service\sketch.json')
            with open('app\service\sketch.json', 'w', encoding='utf-8') as file:
                sketch = file.read()

        item = await ItemLayer().create(sketch, type_sketch='str')

        




