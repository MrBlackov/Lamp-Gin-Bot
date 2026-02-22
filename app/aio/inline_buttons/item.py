from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.db.models.item import ItemSketchDB, ItemDB
from app.db.models.char import CharacterDB
from app.aio.cls.callback.item import (NewItemACtionCall, 
                                       NewItemBackCall,
                                       NewItemAdminACtionCall,
                                       ListItemSketchBackCall, 
                                       ListItemSketchToListCall, 
                                       ListItemSketchToPageCall, 
                                       ListItemSketchToQueryCall,
                                       ListItemSketchItemCall,
                                       ChangeItemSketchCall,
                                       ChangeItemSketchDeleteItemsCall,
                                       ChangeItemSketchDeleteSketchCall,
                                       ChangeItemSketchBackCall,
                                       ChangeItemSketchItemCall,
                                       ChangeItemSketchToPageCall,
                                       ChangetemSketchItemInCharCall)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class NewItemIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=NewItemBackCall(where=where)).as_markup()

    def to_rules(self):
        self.builder.button(text='📜 Требования', callback_data=NewItemACtionCall(to_read_rules=True))
        self.builder.button(text='📖 FAQ', callback_data=NewItemACtionCall(to_faq=True))
        self.builder.button(text='✅ Согласиться', callback_data=NewItemACtionCall(to_argree_rules=True))
        return self.builder.adjust(1).as_markup()
    
    def to_menu(self, is_admin: bool = False, is_redact: bool = False):
        self.builder.button(text='🪪 Имя', callback_data=NewItemACtionCall(to_redact=True, redact_key='name'))
        self.builder.button(text='🧠 Эмодзи', callback_data=NewItemACtionCall(to_redact=True, redact_key='emodzi'))
        self.builder.button(text='📏 Вес', callback_data=NewItemACtionCall(to_redact=True, redact_key='size'))
        self.builder.button(text='🎯 Редкость', callback_data=NewItemACtionCall(to_redact=True, redact_key='rarity'))
        self.builder.button(text='📉 Мин. выпадения', callback_data=NewItemACtionCall(to_redact=True, redact_key='min_drop'))
        self.builder.button(text='📈 Макс. выпадения', callback_data=NewItemACtionCall(to_redact=True, redact_key='max_drop'))
        self.builder.button(text='📃 Описание', callback_data=NewItemACtionCall(to_redact=True, redact_key='description'))
        self.builder.button(text='📨 Отправить на проверку', callback_data=NewItemACtionCall(to_send=True))
        if is_admin:
            if is_redact:
                self.builder.button(text='👤 Изменить создателя', callback_data=NewItemACtionCall(to_redact=True, redact_key='creator_id'))
            self.builder.button(text='➕ Создать', callback_data=NewItemACtionCall(to_create=True))
        self.builder.button(text='📜 Требования', callback_data=NewItemACtionCall(to_read_rules=True))
        return self.builder.adjust(2, 2, 2, 1).as_markup()

    def moderator_menu(self, sketch_id: int):
        self.builder.button(text='✅ Создать', callback_data=NewItemAdminACtionCall(sketch_id=sketch_id, to_create=True))
        self.builder.button(text='❌ Отказать', callback_data=NewItemAdminACtionCall(sketch_id=sketch_id, to_create=False))
        #self.builder.button(text='✒️ Изменить', callback_data=NewItemAdminACtionCall(sketch_id=sketch_id, to_redact=True))
        return self.builder.adjust(2, 1).as_markup()
            

class ListItemSketchIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ListItemSketchBackCall(where=where))
        return self.builder.adjust(1).as_markup()

    def to_page(self, page: int):
        self.builder.button(text='↩️ Назад', callback_data=ListItemSketchToPageCall(page=page))
        return self.builder.adjust(1).as_markup()

    def start_menu(self):
        self.builder.button(text='🗂️ Все предметы', callback_data=ListItemSketchToListCall())
        self.builder.button(text='🔎 Поиск', callback_data=ListItemSketchToQueryCall())
        return self.builder.adjust(1).as_markup()
    
    def list_items(self, sketchs: list[ItemSketchDB], page: int, max_page: int, where: str):
        for sketch in sketchs:
            self.builder.button(text=f'{sketch.emodzi} {sketch.name}', callback_data=ListItemSketchItemCall(item=sketch.id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ListItemSketchToPageCall(page=page-1).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ListItemSketchToPageCall(page=page+1).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ListItemSketchBackCall(where=where).pack()))
        return self.builder.as_markup()        

class ChangeItemSketchIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where=where))
        return self.builder.adjust(1).as_markup()

    def charnge_item(self):
        self.builder.button(text='🪪 Имя', callback_data=ChangeItemSketchCall(what='name'))
        self.builder.button(text='⏲️ Вес', callback_data=ChangeItemSketchCall(what='size'))
        self.builder.button(text='💠 Эмодзи', callback_data=ChangeItemSketchCall(what='emodzi'))
        self.builder.button(text='📜 Описание', callback_data=ChangeItemSketchCall(what='description'))
        self.builder.button(text='🗃️ Обладатели предмета', callback_data=ChangeItemSketchCall(to_items=True))
        self.builder.button(text='✂️ Удалить предметы', callback_data=ChangeItemSketchDeleteItemsCall())
        self.builder.button(text='🗑️ Удалить эскиз', callback_data=ChangeItemSketchDeleteSketchCall())

        return self.builder.adjust(2, 2, 1).as_markup()

    def to_items(self, datas: tuple[tuple[CharacterDB, ItemDB]], page: int, max_page: int, where: str):
        for data in datas:
            char, item = data
            self.builder.button(text=f'💮 {char.exist.full_name} [{char.id}]', callback_data=ChangeItemSketchItemCall(item_id=item.id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ChangeItemSketchToPageCall(page=page-1).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ChangeItemSketchToPageCall(page=page+1).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ChangeItemSketchBackCall(where=where).pack()))
        return self.builder.as_markup()  
    
    def to_delete_items(self, where: str):
        self.builder.button(text='✅ Да', callback_data=ChangeItemSketchDeleteItemsCall(is_delete=True))
        self.builder.button(text='❌ Нет', callback_data=ChangeItemSketchBackCall(where=where))
        return self.builder.adjust(2).as_markup()

    def to_delete_sketch(self, where: str):
        self.builder.button(text='✅ Да', callback_data=ChangeItemSketchDeleteSketchCall(is_delete=True))
        self.builder.button(text='❌ Нет', callback_data=ChangeItemSketchBackCall(where=where))
        return self.builder.adjust(2).as_markup()

    def actions_inventory(self, item_id: int, where: str):
        self.builder.button(text='➕ Дать', callback_data=ChangetemSketchItemInCharCall(item_id=item_id, action='+'))
        self.builder.button(text='➖ Забрать', callback_data=ChangetemSketchItemInCharCall(item_id=item_id, action='-'))
        self.builder.button(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where=where))
        return self.builder.adjust(2, 1).as_markup()    
    


        
        