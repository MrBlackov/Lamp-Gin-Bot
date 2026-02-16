from app.service.base import BaseService
from aiogram.types import Document
from app.aio.config import bot
from app.service.utils import str_to_json, to_msg
from app.logic.query import LetterSearch
from app.aio.inline_buttons.transfer import ItemTransferIKB, InfoTransferIKB
from app.interlayer.transfer import TransferLayer
from app.interlayer.char import InventoryCharacterLayer
from app.db.models.char import CharacterDB
from app.aio.cls.fsm.transfer import ItemTransferState, InfoTransferState
from app.aio.msg.transfer import ItemTransferText, InfoTransferText, TextHTML
from app.aio.msg.item import ItemSketchText, ItemSketchDB, ItemDB
from app.aio.config import admins
from app.exeption.transfer import TransferQuantityNoIntError, TransferError, TransferNoHaventItemError
from app.logic.cls import MyTransfers
from app.db.models.transfer import TransferDB
from app.logged.infolog import infolog
from app.aio.msg.base import UserText

class NewItemTransferService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = ItemTransferIKB()
        self.layer = TransferLayer(tg_id)
        self.text = ItemTransferText
        
    async def new_transfer(self):
        return '📲 Выберите режим сделки:', self.IKB.new_transfer()

    async def new_trade(self):
        all_chars = await self.layer.locator()
        chars = {char.id:char for char in all_chars}
        await self.state.update_data(chars=chars, back_where='to_trade')
        return '❔ С каким персонажем заключим сделку?', self.IKB.choise_char('cmd')
    
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
        return '✒️ Отправьте имя искомого персонажа', self.IKB.back(back_where)

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
        return '😕 Ничего не найдено', self.IKB.back(back_where)

    async def to_page_char(self, page: int):
        back_where = await self.state.get_value('back_where')
        pages = await self.state.get_value('chars_pages')
        max_page = len(pages)
        await self.state.update_data(charpage=page)
        return f'🧭 Персонажи поблизости {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.charpage(pages[page], page, max_page, back_where)

    async def trade_menu(self, char_id: int | None = None, char1: CharacterDB | None = None, char2: CharacterDB | None = None):
        if char_id:
           char_dict: dict[int, CharacterDB] = await self.state.get_value('chars')
           char2 = char_dict.get(char_id)
           char_info = await InventoryCharacterLayer(self.tg_id).get_char_info()
           char1 = char_info.char
        await self.state.update_data(char1=char1, char2=char2)
        items1 = await self.state.get_value('items1')
        items2 = await self.state.get_value('items2')
        return self.text(char1, char2, 
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
        return f'📦 Предметы {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.itempage(pages[page], page, max_page, back_where, side)

    async def to_item_info(self, item_id: int, msg):
        item = (await self.state.get_value('items_dict')).get(item_id)
        await self.state.update_data(item_id=item_id)
        await self.state.set_state(ItemTransferState.item_quantity)
        await self.state.update_data(msg = msg)
        return ItemSketchText(item).text(True if self.tg_id == admins else False) + '\n \n ✒️ Отправьте количество', self.IKB.back('item_page')

    async def item_quantity(self, quantity: str):
        if quantity.isdigit() == False:
            raise TransferQuantityNoIntError(f'This user(tg_id={self.tg_id}) enter quantity to transfer no int')
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
        bayer_tg_id, user, trade = await self.layer.newtrade(char1, char2, 
                                                [item for item in items1.values()] if items1 else None, 
                                                [item for item in items2.values()] if items2 else None, 'confirmed')

        await to_msg(bayer_tg_id, f'✅ Пришла сделка для {char2.exist.full_name}, посмотреть /transfer')
        await infolog.new_transfer(self.tg_id, UserText(user.tg_user, user).text + '\n \n' + self.text(char1, char2, 
                                [item for item in items1.values()] if items1 else None, 
                                [item for item in items2.values()] if items2 else None,
                                ).text('🟢', '🔵'))
        return '✅ Сделка отправлена, посмотреть свои сделки /transfer', None

    async def to_created(self):
        char1: CharacterDB = await self.state.get_value('char1')
        char2: CharacterDB = await self.state.get_value('char2')
        items1 = await self.state.get_value('items1')
        items2 = await self.state.get_value('items2')
        bayer_tg_id = await self.layer.newtrade(char1, char2, 
                                                [item for item in items1.values()] if items1 else None, 
                                                [item for item in items2.values()] if items2 else None, 'created')
        return '💾 Сделка сохранена в виде черновика, посмотреть свои сделки - /transfer', None    


class InfoTransferService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = InfoTransferIKB()
        self.layer = TransferLayer(tg_id)
        self.text = ItemTransferText

    async def main_menu(self):
        transfers = await self.layer.transfers()
        print(transfers)
        await self.state.update_data(transfers=transfers, back_where='cmd')
        return f'🗂️ Ваши сделки ({transfers.quantity} шт.)', self.IKB.menu()

    async def to_transfer(self, status_name: str):
        status = MyTransfers().get_status(status_name)
        print(status.name)
        mytransfers: MyTransfers = await self.state.get_value('transfers')
        print(mytransfers)
        await self.state.update_data(text=status.text)
        from_me = mytransfers.from_me
        to_me = mytransfers.to_me
        
        if status.name == 'received':
            transfers = [transfer for transfer in to_me if transfer.status == 'confirmed']
        elif status.name == 'confirmed':
            transfers = [transfer for transfer in from_me if transfer.status == 'confirmed']
        else:
            transfers = [transfer for transfer in to_me if transfer.status == status.name] + [transfer for transfer in from_me if transfer.status == status.name]
            
        return await self.to_list_transfer(transfers)

    async def to_pages(self):
        return await self.to_page_transfer(0)

    async def to_list_transfer(self, transfers: list[TransferDB] | None, values_in_page: int = 10):
        if transfers == None or len(transfers) < 1:
            return '😕 Тут пусто', self.IKB.back('cmd')
        pages = [tuple(transfers[i:i+values_in_page]) for i in range(0, len(transfers), values_in_page)]
        await self.state.update_data(transfer_pages=pages)
        return await self.to_page_transfer(0)

    async def to_page_transfer(self, page: int):
        back_where = await self.state.get_value('back_where')
        pages = await self.state.get_value('transfer_pages')
        text = await self.state.get_value('text')
        layer = await self.layer.get_char_info()
        max_page = len(pages)
        return f'{text} {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.pages(layer.char_id, pages[page], page, max_page, back_where)

    async def to_search(self, search_type: str, msg):
        print(search_type)
        await self.state.set_state(InfoTransferState.search)
        await self.state.update_data(search_type=search_type, msg=msg)
        return InfoTransferText.search_text(search_type), self.IKB.back('cmd')

    async def search(self, query: str):
        search_type = await self.state.get_value('search_type')
        print(search_type)
        result = await self.layer.search(query, search_type)
        if type(result) == MyTransfers:
            transfers = result.all
        elif type(result) == TransferDB:
            transfers = [result]
        else:
            raise TransferError('Unknown transfer type')

        await self.state.update_data(text = f'🔎 Найденные сделки ({len(transfers)} шт.)', )             
        return await self.to_list_transfer(transfers)

    async def transfer(self, transfer_id: int):
        back_where = await self.state.get_value('back_where')
        mytransfers: MyTransfers = await self.layer.transfers()
        char = (await self.layer.get_char_info()).char_info
        transfer = mytransfers.all_for_id.get(transfer_id)
        items = await self.layer.get_items(transfer_id)
        if transfer.status == 'created':
            buttons = self.IKB.to_create(transfer_id, back_where)
        elif transfer.status == 'confirmed' and char.id != transfer.buyer.id:
            buttons = self.IKB.to_confirm(transfer_id, back_where)
        elif transfer.status == 'confirmed' and char.id == transfer.buyer.id:
            buttons = self.IKB.to_complete(transfer_id, back_where)
        elif transfer.status in ['rejected', 'completed']:
            buttons = self.IKB.back(back_where)
        else:
            raise TransferError('Unknown transfer status')
        return ItemTransferText(transfer.seller, transfer.buyer, items.from_me_items, items.to_me_items).text('🟢', '🔵'), buttons

    async def new_status(self, transfer_id: int, new_status: str):
        layer = await self.layer.update_status(transfer_id, new_status)
        if layer.transfer.status == 'confirmed': 
            await to_msg(layer.user_tg.tg_id, f'✅ Вам пришла новая сделка, посмотреть - {InfoTransferText.to_transfer_id(transfer_id)}')
            return f'✅ Сделка отправлена', self.IKB.back('cmd')
        elif layer.transfer.status == 'rejected': 
            await to_msg(layer.user_tg.tg_id, f'❌ Одна из сделок была отозвана, посмотреть - {InfoTransferText.to_transfer_id(transfer_id)}')
            return f'❌ Сделка отозвана', self.IKB.back('cmd')
        else: 
            await to_msg(layer.user_tg.tg_id, f'🔄️ Статус сделки был изменен, посмотреть - {InfoTransferText.to_transfer_id(transfer_id)}')
            return f'🔄️ Статус сделки изменен на {new_status}', self.IKB.back('cmd')
   
    async def to_complete(self, transfer_id: int):
        seller_user, user, my_char = await self.layer.transfer_complete(transfer_id)
        await to_msg(user.tg_id, f'✅ Сделка была заключена, посмотреть - {InfoTransferText.to_transfer_id(transfer_id)}')
        return '✅ Сделка заключена', self.IKB.back('cmd')

    async def to_delete(self, transfer_id: int):
        await self.layer.delete_transfer(transfer_id)
        return '🗑️ Сделка удалена', self.IKB.back('cmd')

    async def to_redact(self, transfer_id: int):
        mytransfers: MyTransfers = await self.layer.transfers()
        transfer = mytransfers.all_for_id.get(transfer_id)
        if transfer.status == 'created':
            await self.to_delete(transfer_id)
        await self.state.clear()
        await self.state.update_data(items1=transfer.seller_items, items2=transfer.buyer_items, redact_transfer=transfer)
        await self.new_status(transfer_id, 'rejected')
        return await NewItemTransferService(self.tg_id, self.state).trade_menu(char1=transfer.seller, char2=transfer.buyer)




    async def to_transfer_for_id(self, transfer_id: str):
        if transfer_id.isdigit() == False:
            raise TransferQuantityNoIntError(f'This user(tg_id={self.tg_id}) enter quantity to transfer no int')
        await self.state.update_data(back_where='cmd', search_type='transfer_id', text='📂 Ваша сделка')
        return await self.search(transfer_id)


class TransferService:
    def __init__(self, tg_id: int, state = None):
        self.new = NewItemTransferService(tg_id, state)
        self.info = InfoTransferService(tg_id, state)
        


