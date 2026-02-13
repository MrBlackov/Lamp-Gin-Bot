from app.service.base import BaseService
from aiogram.types import Document
from app.aio.config import bot
from app.service.utils import str_to_json
from app.logic.query import LetterSearch
from app.aio.inline_buttons.transfer import ItemTransferIKB
from app.interlayer.transfer import TransferLayer
from app.interlayer.char import InventoryCharacterLayer
from app.db.models.char import CharacterDB
from app.aio.cls.fsm.transfer import ItemTransferState
from app.aio.msg.transfer import ItemTransferText
from app.aio.msg.item import ItemSketchText, ItemSketchDB, ItemDB
from app.aio.config import admins
from app.exeption.transfer import TransferQuantityNoInt

class ItemTransferService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = ItemTransferIKB()
        self.layer = TransferLayer(tg_id)
        self.text = ItemTransferText
        
    async def new_transfer(self):
        return 'Выбериже режим сделки:', self.IKB.new_transfer()

    async def new_trade(self):
        all_chars = await self.layer.locator()
        chars = {char.id:char for char in all_chars}
        await self.state.update_data(chars=chars, back_where='to_trade')
        return 'С каким персонажем заключим сделку?', self.IKB.choise_char('cmd')
    
    async def to_list_char(self, values_in_page: int = 5):
        char_dict: dict[int, CharacterDB] = await self.state.get_value('chars')
        chars = [c for i, c in char_dict.items()]
        pages = [tuple(chars[i:i+values_in_page]) for i in range(0, len(chars), values_in_page)]
        await self.state.update_data(chars_pages=pages)
        return await self.to_page_char(0)

    async def to_search_char(self, msg):
        back_where = await self.state.get_value('back_where')
        await self.state.update_data(msg=msg)
        await self.state.set_state(ItemTransferState.search_char)
        return 'Отправьте имя искомого персонажа', self.IKB.back(back_where)

    async def search_char(self, find: str, values_in_page: int = 5):
        back_where = await self.state.get_value('back_where')
        chars: dict[int, CharacterDB] = await self.state.get_value('chars')
        search_data = LetterSearch([c.exist.full_name for i, c in chars.items()]).search(find)
        if search_data:
            chars_name = {c.exist.full_name.lower():c for i, c in chars.items()}
            search_chars = [chars_name[name] for name in search_data]
            pages = [tuple(search_chars[i:i+values_in_page]) for i in range(0, len(search_chars), values_in_page)]
            await self.state.update_data(chars_pages=pages)
            return await self.to_page_char(0)
        return 'Ничего не найдено', self.IKB.back(back_where)

    async def to_page_char(self, page: int):
        back_where = await self.state.get_value('back_where')
        pages = await self.state.get_value('chars_pages')
        max_page = len(pages)
        await self.state.update_data(charpage=page)
        return f'Персонажи поблизости {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.charpage(pages[page], page, max_page, back_where)

    async def trade_menu(self, char_id: int):
        char_dict: dict[int, CharacterDB] = await self.state.get_value('chars')
        char2 = char_dict.get(char_id)
        char_info = await InventoryCharacterLayer(self.tg_id).get_char_info()
        char1 = char_info.char
        await self.state.update_data(char1=char1, char2=char2)
        items1 = await self.state.get_value('items1')
        items2 = await self.state.get_value('items2')
        return ItemTransferText(char1, char2, 
                                [item for item in items1.values()] if items1 else None, 
                                [item for item in items2.values()] if items2 else None,
                                ).text('🟢', '🔵'), self.IKB.menu('🟢', '🔵')



    async def add_item(self, action: str, side: int):
        if action == '+':
            items = await self.layer.item_sketch.get_sketchs()
            items_dict = {item.id: item for item in items}
        else:
            items_dict0 = await self.state.get_value('items1' if side == 1 else 'items2')
            if items_dict0 == None:
                return '❌ Сначала добавьте предметы', self.IKB.back('trade_menu')
            items_dict = {id: item.sketch for id, item in items_dict0.items()}
            items = [item.sketch for item in items_dict0.values()]
        await self.state.update_data(items=items, action=action, items_dict=items_dict, side=side, back_where='trade_menu')
        return await self.to_list_items()

    async def to_list_items(self, values_in_page: int = 10):
        items: list[dict] = await self.state.get_value('items')
        pages = [tuple(items[i:i+values_in_page]) for i in range(0, len(items), values_in_page)]
        await self.state.update_data(items_pages=pages)
        return await self.to_page_item(0)

    async def to_page_item(self, page: int):
        back_where = await self.state.get_value('back_where')
        side = await self.state.get_value('side')
        pages = await self.state.get_value('items_pages')
        max_page = len(pages)
        await self.state.update_data(itempage=page)
        return f'Предметы {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.itempage(pages[page], page, max_page, back_where, side)

    async def to_item_info(self, item_id: int, msg):
        item = (await self.state.get_value('items_dict')).get(item_id)
        await self.state.update_data(item_id=item_id)
        await self.state.set_state(ItemTransferState.item_quantity)
        await self.state.update_data(msg = msg)
        return ItemSketchText(item).text(True if self.tg_id == admins else False) + '\n \n Отправьте количество', self.IKB.back('item_page')

    async def item_quantity(self, quantity: str):
        if quantity.isdigit() == False:
            raise TransferQuantityNoInt(f'This user(tg_id={self.tg_id}) enter quantity to transfer no int')
        action = await self.state.get_value('action')
        item_id = await self.state.get_value('item_id')
        sketch = (await self.state.get_value('items_dict')).get(item_id)
        side = await self.state.get_value('side')
        products: dict[int, ItemDB] = await self.state.get_value('items1' if side == 1 else 'items2')
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

        await self.state.update_data(**{('items1' if side == 1 else 'items2'):products})
        char = await self.state.get_value('char2')
        char_id = char.id   
        return await self.trade_menu(char_id)
    

    async def to_send(self):
        char1: CharacterDB = await self.state.get_value('char1')
        char2: CharacterDB = await self.state.get_value('char2')
        items1 = await self.state.get_value('items1')
        items2 = await self.state.get_value('items2')
        bayer_tg_id = await self.layer.newtrade(char1, char2, [item for item in items1.values()], [item for item in items2.values()])
        await bot.send_message(bayer_tg_id, f'Пришла сделка для {char2.exist.full_name}, посмотреть /transfer')
        return 'Сделка отправлена, посмотреть свои сделки /transfer', None
    


