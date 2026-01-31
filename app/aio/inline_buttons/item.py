from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.db.models.item import ItemSketchDB
from app.aio.cls.callback.item import (AddItemBackCall, 
                                       AddItemTypeCall, 
                                       AddItemMisskCall, 
                                       AddItemToCreate, 
                                       ListItemSketchBackCall, 
                                       ListItemSketchToListCall, 
                                       ListItemSketchToPageCall, 
                                       ListItemSketchToQueryCall,
                                       ListItemSketchItemCall,
                                       ChangeItemSketchCall,
                                       ChangeItemSketchDeleteItemsCall,
                                       ChangeItemSketchDeleteSketchCall)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AddItemIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=AddItemBackCall(where=where))

    def to_miss(self, back_where: str, next_where: str | None = None):
        if next_where:
            self.builder.button(text='❌ Пропустить', callback_data=AddItemMisskCall(where=next_where))
        self.back(back_where)
        return self.builder.adjust(1).as_markup()
    
    def to_check(self, where: str):
        self.builder.button(text='✅ Создать', callback_data=AddItemToCreate())
        self.back(where)
        return self.builder.adjust(1).as_markup()
    
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
        self.builder.button(text='↩️ Назад', callback_data=ListItemSketchBackCall(where=where))
        return self.builder.adjust(1).as_markup()

    def charnge_item(self):
        self.builder.button(text=' Имя', callback_data=ChangeItemSketchCall(is_name=True))
        self.builder.button(text=' Вес', callback_data=ChangeItemSketchCall(is_size=True))
        self.builder.button(text=' Эмодзи', callback_data=ChangeItemSketchCall(is_emodzi=True))
        self.builder.button(text=' Описание', callback_data=ChangeItemSketchCall(is_desc=True))
        self.builder.button(text=' Удалить эскиз', callback_data=ChangeItemSketchDeleteSketchCall())
        self.builder.button(text=' Удалить предметы', callback_data=ChangeItemSketchDeleteItemsCall())

        return self.builder.adjust(2, 2, 1).as_markup()

    def to_delete_item(self):
        return    


    


        
        