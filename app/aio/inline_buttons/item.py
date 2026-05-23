from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.db.models.item import ItemSketchDB, ItemDB
from app.db.models.char import CharacterDB
from app.aio.cls.callback.item import (NewItemACtionCall, 
                                       NewItemBackCall,
                                       NewItemAdminACtionCall,
                                       NewItemSketchDeleteActionTagCall,
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
                                       ChangetemSketchItemInCharCall, 
                                       ChangeItemSketchIDCall,
                                       GiveItemCall,
                                       GiveItemActionCall,
                                       GiveItemBackCall,
                                       ChangeItemSketchAddActionTagCall,
                                       ChangeItemSketchDeleteActionTagCall,
                                       MenuCall)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class NewItemIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=NewItemBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def cancel(self):
        return self.builder.button(text='❌ Отменить создание', callback_data=NewItemBackCall(where='cancel', tg_id=self.tg_id)).as_markup()
 
    def to_rules(self):
        self.builder.button(text='📖 FAQ по предметам', callback_data=NewItemACtionCall(to_faq=True, tg_id=self.tg_id))
        self.builder.button(text='📜 Требования', callback_data=NewItemACtionCall(to_read_rules=True, tg_id=self.tg_id))
        self.builder.button(text='✅ Согласиться', callback_data=NewItemACtionCall(to_argree_rules=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def to_menu(self, is_admin: bool = False, is_redact: bool = False):
        self.builder.button(text='🏷️ Тэг', callback_data=NewItemACtionCall(what='tag', tg_id=self.tg_id))
        self.builder.button(text='🪪 Имя', callback_data=NewItemACtionCall(to_redact=True, redact_key='name', tg_id=self.tg_id))
        self.builder.button(text='🧠 Эмодзи', callback_data=NewItemACtionCall(to_redact=True, redact_key='emodzi', tg_id=self.tg_id))
        self.builder.button(text='📏 Вес', callback_data=NewItemACtionCall(to_redact=True, redact_key='size', tg_id=self.tg_id))
        #self.builder.button(text='🎯 Редкость', callback_data=NewItemACtionCall(to_redact=True, redact_key='rarity', tg_id=self.tg_id))
        #self.builder.button(text='📉 Мин. выпадения', callback_data=NewItemACtionCall(to_redact=True, redact_key='min_drop', tg_id=self.tg_id))
        #self.builder.button(text='📈 Макс. выпадения', callback_data=NewItemACtionCall(to_redact=True, redact_key='max_drop', tg_id=self.tg_id))
        self.builder.button(text='🎟️ Действия', callback_data=NewItemACtionCall(to_action_tags=True, tg_id=self.tg_id))
        self.builder.button(text='📑 NBT', callback_data=NewItemACtionCall(to_nbt=True, tg_id=self.tg_id))
        self.builder.button(text='📃 Описание', callback_data=NewItemACtionCall(to_redact=True, redact_key='description', tg_id=self.tg_id))
        self.builder.button(text='📨 Отправить на проверку', callback_data=NewItemACtionCall(to_send=True, tg_id=self.tg_id))
        if is_admin:
            if is_redact:
                self.builder.button(text='👤 Изменить создателя', callback_data=NewItemACtionCall(to_redact=True, redact_key='creator_id', tg_id=self.tg_id))
            self.builder.button(text='➕ Создать', callback_data=NewItemACtionCall(to_create=True, tg_id=self.tg_id))
        self.builder.button(text='📜 Требования', callback_data=NewItemACtionCall(to_read_rules=True, tg_id=self.tg_id))
        self.builder.button(text='📖 FAQ по предметам', callback_data=NewItemACtionCall(to_faq=True, tg_id=self.tg_id))
        return self.builder.adjust(2, 2, 2, 1).as_markup()

    def moderator_menu(self, sketch_id: int):
        self.builder.button(text='❌ Отказать', callback_data=NewItemAdminACtionCall(sketch_id=sketch_id, to_create=False, tg_id=self.tg_id))
        self.builder.button(text='✅ Создать', callback_data=NewItemAdminACtionCall(sketch_id=sketch_id, to_create=True, tg_id=self.tg_id))
        self.builder.button(text='✏️ Редактировать', callback_data=NewItemAdminACtionCall(redact_item=True, sketch_id=sketch_id, tg_id=self.tg_id))
        return self.builder.adjust(2, 1).as_markup()

    def action_list(self, action_tags: list[str]):
        if action_tags:
            for action_tag in action_tags:
                self.builder.button(text=action_tag, callback_data=NewItemSketchDeleteActionTagCall(tag=action_tag, tg_id=self.tg_id))
        self.builder.adjust(3, repeat=True)
        self.builder.row(InlineKeyboardButton(text='➕ Добавить дейстие', callback_data=NewItemACtionCall(to_add_action=True, tg_id=self.tg_id).pack()))     
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=NewItemBackCall(where='menu', tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
 
    def to_delete_action_tag(self, tag: str):
        self.builder.button(text='❌ Нет', callback_data=NewItemBackCall(where='action', tg_id=self.tg_id))
        self.builder.button(text='✅ Да', callback_data=NewItemSketchDeleteActionTagCall(tag=tag, is_delete=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def to_delete_nbt(self):
        self.builder.button(text='❌ Нет', callback_data=NewItemBackCall(where='nbt', tg_id=self.tg_id))
        self.builder.button(text='✅ Да', callback_data=NewItemACtionCall(delete_nbt=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()
    
    def nbt(self):
        self.builder.button(text='✏️ Изменить', callback_data=NewItemACtionCall(redact_key='nbt', to_redact=True, tg_id=self.tg_id))
        self.builder.button(text='🗑️ Очистить', callback_data=NewItemACtionCall(to_delete_nbt=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewItemBackCall(where='menu', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    



class GiveItemSketchIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=GiveItemBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def menu(self):
        self.builder.button(text='➕ Выдать', callback_data=GiveItemActionCall(to_give=True, tg_id=self.tg_id))
        self.builder.button(text='✏️ Изменить количество', callback_data=GiveItemActionCall(to_quantity=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
class ListItemSketchIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ListItemSketchBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def to_page(self, sketch_id: int, page: int, is_admin: bool = False):
        if is_admin:
            self.builder.button(text='✏️ Редактировать', callback_data=ChangeItemSketchIDCall(sketch_id=sketch_id, tg_id=self.tg_id))
            self.builder.button(text='➕ Выдать', callback_data=GiveItemCall(sketch_id=sketch_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ListItemSketchToPageCall(page=page, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def start_menu(self, is_admin: bool = False):
        self.builder.button(text='🗂️ Все предметы', callback_data=ListItemSketchToListCall(tg_id=self.tg_id))
        if is_admin:
            self.builder.button(text='🌫️ Скрытые предметы', callback_data=ListItemSketchToListCall(is_hide=True, tg_id=self.tg_id))
        self.builder.button(text='🔎 Поиск', callback_data=ListItemSketchToQueryCall(tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def list_items(self, sketchs: list[ItemSketchDB], page: int, max_page: int, where: str):
        for sketch in sketchs:
            self.builder.button(**sketch.button_text, callback_data=ListItemSketchItemCall(item=sketch.id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ListItemSketchToPageCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ListItemSketchToPageCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ListItemSketchBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()        

class ChangeItemSketchIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def charnge_item(self):
        self.builder.button(text='🏷️ Тэг', callback_data=ChangeItemSketchCall(what='tag', tg_id=self.tg_id))
        self.builder.button(text='🪪 Имя', callback_data=ChangeItemSketchCall(what='name', tg_id=self.tg_id))
        self.builder.button(text='💠 Эмодзи', callback_data=ChangeItemSketchCall(what='_emodzi', tg_id=self.tg_id))
        self.builder.button(text='⏲️ Вес', callback_data=ChangeItemSketchCall(what='size', tg_id=self.tg_id))
        self.builder.button(text='🎯 Редкость', callback_data=ChangeItemSketchCall(what='rarity', tg_id=self.tg_id))
        self.builder.button(text='📉 Мин. выпадения', callback_data=ChangeItemSketchCall(what='min_drop', tg_id=self.tg_id))
        self.builder.button(text='📈 Макс. выпадения', callback_data=ChangeItemSketchCall(what='max_drop', tg_id=self.tg_id))
        self.builder.button(text='🎟️ Действия', callback_data=ChangeItemSketchCall(what='action_tag', tg_id=self.tg_id))
        self.builder.button(text='📑 NBT', callback_data=ChangeItemSketchCall(what='nbt', to_nbt=True, tg_id=self.tg_id))
        self.builder.button(text='📜 Описание', callback_data=ChangeItemSketchCall(what='description', tg_id=self.tg_id))
        self.builder.button(text='👁️ Поменять видимость', callback_data=ChangeItemSketchCall(what='is_hide', tg_id=self.tg_id))
        self.builder.button(text='🗃️ Обладатели предмета', callback_data=ChangeItemSketchCall(to_items=True, tg_id=self.tg_id))
        self.builder.button(text='✂️ Удалить предметы', callback_data=ChangeItemSketchDeleteItemsCall(tg_id=self.tg_id))
        self.builder.button(text='🗑️ Удалить эскиз', callback_data=ChangeItemSketchDeleteSketchCall(tg_id=self.tg_id))
        return self.builder.adjust(1, 2, 2, 2, 2, 1).as_markup()

    def action_list(self, action_tags: list[str]):
        if action_tags:
            for action_tag in action_tags:
                self.builder.button(text=action_tag, callback_data=ChangeItemSketchDeleteActionTagCall(tag=action_tag, tg_id=self.tg_id))
        self.builder.adjust(3, repeat=True)
        self.builder.row(InlineKeyboardButton(text='➕ Добавить дейстие', callback_data=ChangeItemSketchAddActionTagCall(tg_id=self.tg_id).pack()))     
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where='info', tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
 
    def to_delete_action_tag(self, tag: str):
        self.builder.button(text='❌ Нет', callback_data=ChangeItemSketchBackCall(where='action', tg_id=self.tg_id))
        self.builder.button(text='✅ Да', callback_data=ChangeItemSketchDeleteActionTagCall(tag=tag, is_delete=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def nbt(self):
        self.builder.button(text='✏️ Изменить', callback_data=ChangeItemSketchCall(what='nbt', tg_id=self.tg_id))
        self.builder.button(text='🗑️ Очистить', callback_data=ChangeItemSketchCall(what='nbt', to_delete_nbt=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where='info', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def to_items(self, datas: tuple[tuple[CharacterDB, ItemDB]], page: int, max_page: int, where: str):
        for data in datas:
            char, item = data
            self.builder.button(text=f'💮 {char.exist.full_name} [{char.id}]', callback_data=ChangeItemSketchItemCall(item_id=item.id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ChangeItemSketchToPageCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ChangeItemSketchToPageCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ChangeItemSketchBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()  
    
    def to_delete_items(self, where: str):
        self.builder.button(text='❌ Нет', callback_data=ChangeItemSketchBackCall(where=where, tg_id=self.tg_id))
        self.builder.button(text='✅ Да', callback_data=ChangeItemSketchDeleteItemsCall(is_delete=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def to_delete_sketch(self, where: str):
        self.builder.button(text='❌ Нет', callback_data=ChangeItemSketchBackCall(where=where, tg_id=self.tg_id))
        self.builder.button(text='✅ Да', callback_data=ChangeItemSketchDeleteSketchCall(is_delete=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()

    def actions_inventory(self, item_id: int, where: str):
        self.builder.button(text='➕ Дать', callback_data=ChangetemSketchItemInCharCall(item_id=item_id, action='+', tg_id=self.tg_id))
        self.builder.button(text='➖ Забрать', callback_data=ChangetemSketchItemInCharCall(item_id=item_id, action='-', tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ChangeItemSketchBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(2, 1).as_markup()    
    


        
        