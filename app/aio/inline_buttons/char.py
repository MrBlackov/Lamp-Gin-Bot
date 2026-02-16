from app.aio.cls.callback.char import (
                                       AddCharGenderCall,  
                                       AddCharNameCall, 
                                       AddCharQueryNameCall, 
                                       AddCharRandomNameCall,
                                       AddCharSketch,
                                       AddCharDescript,
                                       AddCharFinish,
                                       InfoCharList,
                                       InfoCharChouse,
                                       InventoryItems,
                                       InventoryItemsGo, 
                                       InventoryItemsThrow
                                       )
from app.db.models.item import ItemDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class AddCharIKB(BotIKB):
    
    def query_back(self, first_name: bool = True):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='↩️ Назад', callback_data=AddCharQueryNameCall(back=True, first_name=first_name).pack())]])

    def chouse_gender(self, to_change: bool = False):
        self.builder.button(text='👨 Мужской', callback_data=AddCharGenderCall(gender='M', to_change=to_change))
        self.builder.button(text='👩 Женский', callback_data=AddCharGenderCall(gender='W', to_change=to_change))
        self.builder.adjust(2)
        return self.builder.as_markup()
    
    def chouse_regim_name(self, first_name: bool = True):
        self.builder.button(text='🔍 Поищем', callback_data=AddCharNameCall(regim='query', first_name=first_name))
        self.builder.button(text='🎲 Случайно', callback_data=AddCharNameCall(regim='random', first_name=first_name))
        if not first_name: 
            self.builder.button(text='Пропустить', callback_data=AddCharNameCall(first_name=False, to_pass=True))
        self.builder.button(text='↩️ Назад', callback_data=AddCharNameCall(back=True, first_name=first_name))
        self.builder.adjust(2, 1)
        return self.builder.as_markup()
    
    def get_pages_names(self, texts: list[str], page: int, max_page: int = 1, first_name: bool = True):
        for text in texts:
            self.builder.button(text=text, callback_data=AddCharQueryNameCall(name=text, first_name=first_name))
        self.builder.adjust(*[2 for _ in range(len(texts))])
        arrows_page = []
        if page > 0:
            arrows_page.append(InlineKeyboardButton(text='⬅️', callback_data=AddCharQueryNameCall(page=page-1, next_page=True, first_name=first_name).pack()))
        if page != max_page - 1:
            arrows_page.append(InlineKeyboardButton(text='➡️', callback_data=AddCharQueryNameCall(page=page+1, next_page=True, first_name=first_name).pack()))
            
        if len(arrows_page) > 0: 
            self.builder.row(*arrows_page)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=AddCharQueryNameCall(back=True, first_name=first_name).pack()))
            
        return self.builder.as_markup()        
        
    def get_rnd_name(self, name: str, first_name: bool = True):
        self.builder.button(text='↩️', callback_data=AddCharRandomNameCall(back=True, first_name=first_name))
        self.builder.button(text='🔄️', callback_data=AddCharRandomNameCall(regeneration=True, first_name=first_name))
        self.builder.button(text='✅', callback_data=AddCharRandomNameCall(name=name, first_name=first_name))
        self.builder.adjust(3)
        return self.builder.as_markup()

    def get_sketchs(self, sketch_id: int, max_quantity: int):
        max_quantity -= 1
        self.builder.button(text='↩️', callback_data=AddCharSketch(id=sketch_id, back=True))
        if sketch_id < max_quantity:
            free_quantity = max_quantity - sketch_id
            self.builder.button(text=f'{free_quantity} 🔄️', callback_data=AddCharSketch(id=sketch_id, another=True))
        self.builder.button(text='✅', callback_data=AddCharSketch(id=sketch_id, another=False))
        self.builder.adjust(3)
        return self.builder.as_markup()       

    def descript(self):
        self.builder.button(text='➡️ Пропустить', callback_data=AddCharDescript(to_pass=True))    
        self.builder.button(text='↩️ Назад', callback_data=AddCharDescript(back=True))
        return self.builder.adjust(1).as_markup()
        
    def to_finish(self, gender: str):
        self.builder.button(text='✅ Создать', callback_data=AddCharFinish(go=True))    
        self.builder.button(text='🔁 Изменить', callback_data=AddCharGenderCall(gender=gender, to_change=True))
        return self.builder.adjust(1).as_markup()
    
class InfoCharIKB(BotIKB):
    def get_list(self, main_char_id: int | None, char_dict: dict[int, str]):
        if main_char_id in char_dict:
            main_char = char_dict.pop(main_char_id)
            self.builder.button(text=f'👑 {main_char}', callback_data=InfoCharList(char_id=main_char_id, main=True))
        for char_id, char_name in char_dict.items():
            self.builder.button(text=f'♟️ {char_name}', callback_data=InfoCharList(char_id=char_id))
        return self.builder.adjust(1).as_markup()
            
    def chouse_main_char(self, char_id: int, main: bool = False): 
        self.builder.button(text='↩️ Назад', callback_data=InfoCharChouse(back=True))
        if main == False:
            self.builder.button(text='🕹️ Выбрать', callback_data=InfoCharChouse(char_id=char_id))   
        return self.builder.adjust(2).as_markup()

    @property
    def add_char(self):
        return AddCharIKB()

class InventoryIKB(BotIKB):
    def items(self, items: dict[int, ItemDB]):
        for id, item in items.items():
            self.builder.button(text=f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity})', callback_data=InventoryItems(item=id))
        return self.builder.adjust(1).as_markup()
    
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGo(where=where))
        return self.builder.adjust(2).as_markup()

    def throw(self, where: str):
        self.builder.button(text='🚮 Выбросить', callback_data=InventoryItemsThrow(where=where))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGo(where=where))
        return self.builder.adjust(1).as_markup()