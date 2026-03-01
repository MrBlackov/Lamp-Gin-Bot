from app.service.base import BaseService
from aiogram.types import Document
from app.aio.config import bot, admins
from app.service.utils import str_to_json, to_msg
from app.exeption.base import PermissionError
from app.logged.infolog import infolog
from app.interlayer.craft import CraftLayer
from app.aio.inline_buttons.craft import CraftIKB
from app.aio.msg.craft import CraftText
from app.aio.cls.fsm.craft import CraftState
from app.aio.msg.item import ItemSketchText, ItemDB
from app.exeption.craft import CraftQuantityNoIntError
from app.aio.cls.fsm.utils import CraftFSM

class CraftService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.state = CraftFSM(state)
        self.layer = CraftLayer(tg_id, state)
        self.IKB = CraftIKB()

    async def get_no_hide_craft(self, values_in_page=5):
        crafts = await self.layer.logic.get_crafts(no_hide=True)
        await self.state.update_data(crafts=crafts, back_where='cmd')
        if not crafts:
            return 'Вы не знаете ни одного рецепта', None
        pages = [tuple(crafts[i:i+values_in_page]) for i in range(0, len(crafts), values_in_page)]
        await self.state.update_data(pages=pages)
        return await self.crafts_page(0)
    
    async def crafts_page(self, page: int):         
        pages  = await self.state.get_value('pages')
        max_page = len(pages)
        return f'Известные рецепты [{f'{page}/{max_page}стр.' if max_page > 1 else ''}]', self.IKB.crafts(crafts=pages, page=page, max_page=max_page)

    async def craft(self, craft_id: int):
        craft = await self.layer.logic.get_craft(craft_id=craft_id)
        return CraftText(craft=craft).text, self.IKB.back(where='cmd')
    
    async def add_item(self, action: str, item_type: str):
        if action == '+':
            items = await self.layer.item_sketch.get_sketchs()
            items_dict = {item.id: item for item in items}
        else:
            items_dict0 = await self.state.get_value(item_type)
            if items_dict0 == None:
                return '❌ Сначала добавьте предметы', self.IKB.back('craft_menu')
            items_dict = {id: item.sketch for id, item in items_dict0.items()}
            items = [item.sketch for item in items_dict0.values()]
        await self.state.update_data(items=items, action=action, items_dict=items_dict, item_type=item_type, back_where='craft_menu')
        return await self.to_list_items()

    async def to_list_items(self, values_in_page: int = 10):
        items: list[dict] = await self.state.get_value('items')
        pages = [tuple(items[i:i+values_in_page]) for i in range(0, len(items), values_in_page)]
        await self.state.update_data(items_pages=pages)
        return await self.to_page_item(0)

    async def to_page_item(self, page: int):
        back_where = await self.state.get_value('back_where')
        item_type = await self.state.get_value('item_type')
        pages = await self.state.get_value('items_pages')
        max_page = len(pages)
        await self.state.update_data(itempage=page)
        return f'📦 Предметы {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.itempage(pages[page], page, max_page, back_where, item_type)

    async def to_item_info(self, item_id: int, msg):
        item = (await self.state.get_value('items_dict')).get(item_id)
        await self.state.update_data(item_id=item_id)
        await self.state.set_state(CraftState.item_quantity)
        await self.state.update_data(msg = msg)
        return ItemSketchText(item).text(True if self.tg_id == admins else False) + '\n \n ✒️ Отправьте количество', self.IKB.back('item_page')

    async def item_quantity(self, quantity: str):
        if quantity.isdigit() == False:
            raise CraftQuantityNoIntError(f'This user(tg_id={self.tg_id}) enter quantity to transfer no int')
        action = await self.state.get_value('action')
        item_id = await self.state.get_value('item_id')
        sketch = (await self.state.get_value('items_dict')).get(item_id)
        item_type = await self.state.get_value('item_type')
        products: dict[int, ItemDB] = await self.state.get_value(item_type)
        if products:
            item_product: ItemDB | None = products.pop(item_id, None)
            if item_product:
                quan = item_product.quantity
                if action == '+':
                    quan += int(quantity)
                else:
                    quan -= int(quantity) 

                if quan > 0:
                    item_product.quantity = quan
                    products[item_id] = item_product
    
            elif action == '+':
                item_product = ItemDB(quantity=int(quantity), sketch=sketch, sketch_id=item_id)
                products[item_id] = item_product
        else:
            products = {}
            item_product = ItemDB(quantity=int(quantity), sketch=sketch, sketch_id=item_id)
            products[item_id] = item_product

        await self.state.update_data(**{item_type:products})
        char = await self.state.get_value('char2')
        char_id = char.id   
        return await self.trade_menu(char_id)


