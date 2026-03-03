from app.service.base import BaseService
from app.interlayer.item import ItemLayer
from app.aio.inline_buttons.item import ListItemSketchIKB, ItemSketchDB, ChangeItemSketchIKB, NewItemIKB
from aiogram.types import Document
from app.aio.config import bot, admins
from app.service.utils import str_to_json, to_msg
import json
from app.aio.cls.fsm.item import ListItemSketchsState, ChangeItemSketchState
from app.exeption.item import GiveItemQuantityLessOne, GiveItemNoEnterNameOrID, GiveItemNoInt, GiveItemNoEnterID, ItemNoHideCreatedError
from app.logic.query import LetterSearch
from app.aio.msg.item import ItemSketchText, CharItemText, NewItemText
from app.exeption.item import ThrowAwayQuantityNoInt
from app.exeption.base import PermissionError
from app.aio.msg.base import UserText
from app.aio.cls.fsm.item import NewItemState
from app.validate.sketchs.item_sketchs import ItemSketchValide
from app.logged.infolog import infolog
from app.exeption.item import ItemError
from app.aio.cls.fsm.utils import ItemFSM

class ItemBaseService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = ItemLayer(tg_id)

class AddItemService(ItemBaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.state = ItemFSM(state, 'add')
        self.IKB = NewItemIKB()
        self.text = NewItemText

    async def add_data_item(self, string: str | None = None, document: Document | None = None):
        if string:
            sketch = str_to_json(string)
        elif document:
            tgfile = await bot.get_file(document.file_id)
            await bot.download_file(tgfile.file_path, 'app/service/sketch.json')
            with open('app/service/sketch.json', 'w', encoding='utf-8') as file:
                line = file.read()
            sketch = json.loads(line)
            sketch['is_hide'] = False
        user, item = await self.layer.create(item = sketch)
        if user and item: 
            await infolog.new_item(user.id, UserText(user.tg_user, user).text + ' \n' + ItemSketchText(item).text(True))
            return '✅ Предмет создан, посмотреть /inventory'
        
    async def to_create_item(self):
        return ' Прочитайте требования к будущему эскизу', self.IKB.to_rules()

    async def to_name(self):
        await self.state.set_state(NewItemState.to_name)
        return self.text.to_redact_text('name'), None
    
    async def to_emodzi(self, name: str, msg):
        await self.state.set_state(NewItemState.to_emodzi)
        await self.state.update_data(msg=msg)
        await self.state.update_data(sketch=ItemSketchValide(name=name).model_dump())
        return self.text.to_redact_text('emodzi'), None
    
    async def to_menu(self, emodzi: str):
        return await self.redact_value(emodzi, 'emodzi')
 
    async def to_redact(self, redact_key: str, msg):
        await self.state.set_state(NewItemState.to_redact)
        await self.state.update_data(redact_key=redact_key, msg=msg)
        return self.text.to_redact_text(redact_key), self.IKB.back('menu')

    async def redact(self, value: str):
        key = await self.state.get_value('redact_key')
        return await self.redact_value(value, key)

    async def redact_value(self, value: str, key: str):
        sketch = await self.state.get_value('sketch')
        sketch[key] = value
        await self.state.update_data(sketch=sketch)
        return await self.menu()

    async def menu(self):
        sketch = await self.state.get_value('sketch')
        is_redact = await self.state.get_value('is_redact')
        sketch = ItemSketchValide(**sketch)
        return self.text(sketch).text(), self.IKB.to_menu(True if self.tg_id in self.admins else False, is_redact)

    async def to_send(self):
        sketch = await self.state.get_value('sketch')
        sketch = ItemSketchValide(**sketch).model_dump()
        user, item = await self.layer.create(sketch)
        if user and item:
            await infolog.new_sketch_no_moderate(self.tg_id, UserText(user.tg_user, user).text + '\n' + ItemSketchText(item).text(True), self.IKB.moderator_menu(item.id))
            await self.state.clear_this_state()
            return '✅ Предмет отправлен на модерацию', None
        raise ItemError('Dont have user or item')
        
    async def create(self):
        if self.tg_id not in admins:
            raise PermissionError(f'This user(tg_id:{self.tg_id}) no admin')
        sketch = await self.state.get_value('sketch')
        sketch = ItemSketchValide(**sketch).model_dump()
        sketch['is_hide'] = False
        user, item = await self.layer.create(sketch)
        if user and item:
            await infolog.new_item(user.id, UserText(user.tg_user, user).text + ' \n \n' + ItemSketchText(item).text(True))
            await self.state.clear_this_state()
            return '✅ Предмет создан, проверьте инвентарь - /inventory', None
        raise ItemError('Dont have user or item')
    
    async def create_after_moderating(self, sketch_id: int, to_create: bool):
        try:
            if self.tg_id not in admins:
                raise PermissionError(f'This user(tg_id:{self.tg_id}) no admin')
            user, create, item = await self.layer.create_before_moder(sketch_id, to_create)
            if user and create:
                await to_msg(user.tg_id, f"✅ Ваш эскиз предмета был принят, предмет: {item.emodzi} {item.name}, проверьте инвентарь - /inventory")
                await infolog.new_item(user.id, UserText(user.tg_user, user).text + ' \n' + ItemSketchText(item).text(True))
                return f'✅ Сообщение подтверждения отправлено, предмет: {item.emodzi} {item.name} [id:{item.id}]', None
            elif user:
                await to_msg(user.tg_id, f"❌ Ваш эскиз предмета был отклонен, предмет: {item.emodzi} {item.name}")
                return f'✅ Сообщение отказа отправлено, предмет: {item.emodzi} {item.name} [id:{item.id}]', None
            raise ItemError('Dont have user or item')
        except ItemNoHideCreatedError as e:
            return '✅ Этот предмет уже был промодерирован', None
        except Exception:
            raise
            
    

class ChangeItemService(ItemBaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.state = ItemFSM(state, 'change')
        self.IKB = ChangeItemSketchIKB()

    async def start(self, string: str):
        data = str_to_json(string)
        item_id = data.get('id')
        if item_id == None:
            raise GiveItemNoEnterID(f'This tg_user({self.tg_id}) dont enter id')
        return await self.info(int(item_id))
    
    async def info(self, sketch_id: int):
        item = await self.layer.get_item_sketch(sketch_id)
        await self.state.update_data(sketch_id=item.id)
        return ItemSketchText(item).text(True), self.IKB.charnge_item()

    async def to_sketch(self):
        sketch_id = await self.state.get_value('sketch_id')
        return await self.info(int(sketch_id))

    async def to_change_data(self, what_change: str, msg, back_where: str = 'info'):
        await self.state.update_data(what_change=what_change, msg=msg)
        await self.state.set_state(ChangeItemSketchState.new_data)
        return '✒️ Отправьте новое значение', self.IKB.back(back_where)
    
    async def change_data(self, new_data: str):
        what_change = await self.state.get_value('what_change')
        sketch_id = await self.state.get_value('sketch_id')
        new_data = self.layer.change_data_valid(what_change, new_data)
        sketch = await self.layer.change_sketch(sketch_id, {what_change:new_data})
        await self.state.update_data(sketch_id=sketch.id)
        return ItemSketchText(sketch).text(True), self.IKB.charnge_item()

    async def to_char_items(self, back_where: str = 'info', value_in_page: int = 10, is_back: bool = False):
        sketch_id = await self.state.get_value('sketch_id')
        datas = await self.layer.get_items_for_sketchs(sketch_id)
        if len(datas) > 0:
            items = {item.id:{'char':char, 'item':item} for char, item in datas.items()}
            to_pages = [tuple([k, v]) for k, v in datas.items()]
            pages = [tuple(to_pages[i:i+value_in_page]) for i in range(0, len(to_pages), value_in_page) ]
            await self.state.update_data(datas=datas, pages=pages, items=items)
            if is_back:
                return
            max_page = len(pages)
            return f"📋 Список персонажей с этим предметом {f'(0/{max_page}стр)' if max_page > 1 else ''}", self.IKB.to_items(pages[0], 0, max_page, back_where)
        if is_back:
            return '😕 Какая то ошибка'
        return '😕 Этого предмета нет ни у кого', self.IKB.back(back_where)

    async def to_page(self, page: int = 0, back_where: str = 'cmd'):
        pages = await self.state.get_value('pages')
        await self.state.update_data(page=page)
        max_page = len(pages)
        return f'📦 Предметы {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''} ', self.IKB.to_items(pages[page], page, max_page, back_where)
    
    async def to_item(self, item_id: int, back_where: str = 'char_items'):
        items: dict[int, dict] = await self.state.get_value('items')
        char_and_item = items.get(item_id)
        char = char_and_item.get('char')
        item = char_and_item.get('item')
        return CharItemText(char, item).text, self.IKB.actions_inventory(item.id, back_where)

    async def to_action_inventory(self, msg, item_id: int, action: str, back_where: str = 'item'):  
        await self.state.set_state(ChangeItemSketchState.action_data)      
        await self.state.update_data(msg=msg, action = action, item_id=item_id)
        return '✒️ Отправьте количество', self.IKB.back(back_where)
    
    async def action_inventory(self, quantity: str, back_where: str = 'info'):
        item_id = await self.state.get_value('item_id')
        action = await self.state.get_value('action')
        items: dict[int, dict] = await self.state.get_value('items')
        char_and_item = items.get(item_id)
        char = char_and_item.get('char')
        item = char_and_item.get('item')

        if quantity.isdigit() == False:
            raise ThrowAwayQuantityNoInt(f'This user(tg_id={self.tg_id}) enter no int')

        is_action, item = await self.layer.action(item, char, action, int(quantity))
        if is_action and item:
            await self.to_char_items(is_back=True)
            return await self.to_item(item.id)
        elif is_action == False:
            return await self.to_char_items()
        else:
            raise ItemError(f'Dont have item')


    async def to_delete_sketch(self, back_where: str = 'info'):
        return '❔ Вы точно хотите удалить предмет(эскиз)?', self.IKB.to_delete_sketch(back_where)

    async def to_delete_items(self, back_where: str = 'info'):
        return '❔ Вы точно хотите забрать все предметы?' , self.IKB.to_delete_items(back_where)

    async def delete_sketch(self, back_where: str = 'info'):
        sketch_id = await self.state.get_value('sketch_id')
        is_delete = await self.layer.delete_sketch(sketch_id)
        await self.state.clear_this_state()
        return ('🗑️ Эскиз предмета был удален', None) if is_delete else ('❌ Эскиз предмета не был удален', self.IKB.back(back_where))

    async def delete_items(self, back_where: str = 'info'):
        sketch_id = await self.state.get_value('sketch_id')
        is_delete = await self.layer.delete_items(sketch_id)
        return ('🗑️ Предметы былы удалены' if is_delete else '❌ Предметы не былы удалены'), self.IKB.back(back_where)

class GiveItemService(ItemBaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.state = ItemFSM(state, 'give')

    async def give(self, string: str):
        data = str_to_json(string)
        name = data.get('data')
        item_id: str = data.get('id')
        quantity: str = data.get('quan')
        if quantity == None:
            quantity = data.get('quantity', 1)  

        if name == None and item_id == None:           
            raise GiveItemNoEnterNameOrID(f'This tg_user({self.tg_id}) dont enter id or name')
        if item_id.isdigit() == False:
            raise GiveItemNoInt(f'This tg_user({self.tg_id}) enter no int ID')
        if quantity and type(quantity) == str:         
            if quantity.isdigit() == False:
                raise GiveItemNoInt(f'This tg_user({self.tg_id}) enter no int quantity')

        if int(quantity) < 1:
            raise GiveItemQuantityLessOne(f'This tg_user({self.tg_id}) enter quantity < 1')

        if item_id:
            item = await self.layer.give(int(item_id), quantity=int(quantity))
        elif name:
            item = await self.layer.give(name=name, quantity=int(quantity))

        if item:
            return f'✅ Выдан предмет({item.sketch.name}) в количестве {quantity} шт.'

class ListItemService(ItemBaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.IKB = ListItemSketchIKB()
        self.state = ItemFSM(state)

    async def get_item_sketchs(self, value_in_page: int = 10):
        sketches = await self.layer.get_item_sketchs()
        pages = [tuple(sketches[i:i+value_in_page]) for i in range(0, len(sketches), value_in_page)]
        sketchs_ids = {s.id:s for s in sketches}
        await self.state.update_data(sketches=sketches, searchs=pages, sketch_ids=sketchs_ids)
        return '❔ Что выберем?', self.IKB.start_menu()
    
    async def list_items(self, page: int = 0, back_where: str = 'cmd'):
        sketches = await self.state.get_value('searchs')
        await self.state.update_data(page=page)
        max_page = len(sketches)
        return f'📦 Предметы {f'[{page + 1}/{max_page}стр]' if max_page > 1 else ''}', self.IKB.list_items(sketches[page], page, max_page, back_where)
    
    async def to_item(self, item_id: int):
        sketch_ids: dict = await self.state.get_value('sketch_ids')
        sketch = sketch_ids.get(item_id, None)
        if sketch:
            page = await self.state.get_value('page')
            return ItemSketchText(sketch).text(True if self.tg_id in self.admins else False), self.IKB.to_page(page)

    async def to_search(self, msg, back_where: str = 'cmd'):
        await self.state.update_data(msg=msg)
        await self.state.set_state(ListItemSketchsState.name)
        return '✒️ Отправьте название предмета', self.IKB.back(back_where)
    
    async def search(self, find: str, back_where: str = 'cmd', value_in_page = 10):
        sketches: list[ItemSketchDB] = await self.state.get_value('sketches')
        sketches_dict = {sketch.name.lower():sketch for sketch in sketches}
        sketch_names = [s.name.lower() for s in sketches]
        searchs = LetterSearch(sketch_names).search(find)
        search_sketch = [sketches_dict.get(search) for search in searchs if search in sketch_names]
        pages = [tuple(search_sketch[i:i+value_in_page]) for i in range(0, len(search_sketch), value_in_page)]
        await self.state.update_data(searchs=pages)
        max_pages = len(pages)
        if max_pages > 0:
            return f'📦 Предметы (0/{max_pages}стр)', self.IKB.list_items(pages[0], 0, max_pages, back_where)
        await self.state.set_state(ListItemSketchsState.name)
        return '❌ Предмет не найден. Отправьте другое название', self.IKB.back(back_where)


class ItemService:
    def __init__(self, tg_id, state = None):
        self.add = AddItemService(tg_id, state)
        self.change = ChangeItemService(tg_id, state)
        self.give = GiveItemService(tg_id, state)
        self.list =  ListItemService(tg_id, state)
        





