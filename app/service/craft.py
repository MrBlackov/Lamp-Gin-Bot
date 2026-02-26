from app.service.base import BaseService
from aiogram.types import Document
from app.aio.config import bot, admins
from app.service.utils import str_to_json, to_msg
from app.exeption.base import PermissionError
from app.logged.infolog import infolog
from app.interlayer.craft import CraftLayer
from app.aio.inline_buttons.craft import CraftIKB
from app.aio.msg.craft import CraftText

class CraftService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = CraftLayer(tg_id, state)
        self.IKB = CraftIKB()

    async def get_no_hide_craft(self, values_in_page=5):
        crafts = await self.layer.logic.get_crafts(no_hide=True)
        await self.state.update_data(crafts=crafts, back_where='cmd')
        if not crafts:
            return 'Нет известных рецептов', self.IKB.craft_hiden()
        pages = [tuple(crafts[i:i+values_in_page]) for i in range(0, len(crafts), values_in_page)]
        await self.state.update_data(pages=pages)
        return await self.crafts_page(0)
    
    async def crafts_page(self, page: int):         
        pages  = await self.state.get_value('pages')
        max_page = len(pages)
        return f'Известные рецепты [{f'{page}/{max_page}стр.' if max_page > 1 else ''}]', self.IKB.crafts(crafts=pages, page=page, max_page=max_page)

    async def craft_hiden(self):
        pass

    async def craft(self, craft_id: int):
        craft = await self.layer.logic.get_craft(craft_id=craft_id)
        return CraftText(craft=craft).text, self.IKB.back(where='cmd')