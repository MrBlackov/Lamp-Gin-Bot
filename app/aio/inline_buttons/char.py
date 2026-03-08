from app.aio.cls.callback.char import (
                                       AddCharGenderCall,  
                                       AddCharNameCall, 
                                       AddCharQueryNameCall, 
                                       AddCharRandomNameCall,
                                       AddCharSketchCall,
                                       AddCharDescriptCall,
                                       AddCharFinishCall,
                                       InfoCharListCall,
                                       InfoCharChooseCall,
                                       InventoryItemsCall,
                                       InventoryItemsGoCall, 
                                       InventoryItemsActionCall,
                                       InventoryItemsPickUpCall
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
    
    def get_bonus_char(self, url: str):
        self.builder.button(text='➕ Подписаться', url=url)
        self.builder.button(text='✅ Проверить', callback_data=AddCharNameCall(get_bonus=True))
        return self.builder.adjust(1).as_markup()

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
        self.builder.button(text='↩️', callback_data=AddCharSketchCall(id=sketch_id, back=True))
        if sketch_id < max_quantity:
            free_quantity = max_quantity - sketch_id
            self.builder.button(text=f'{free_quantity} 🔄️', callback_data=AddCharSketchCall(id=sketch_id, another=True))
        self.builder.button(text='✅', callback_data=AddCharSketchCall(id=sketch_id, another=False))
        self.builder.adjust(3)
        return self.builder.as_markup()       

    def descript(self):
        self.builder.button(text='➡️ Пропустить', callback_data=AddCharDescriptCall(to_pass=True))
        self.builder.button(text='↩️ Назад', callback_data=AddCharDescriptCall(back=True))
        return self.builder.adjust(1).as_markup()
        
    def to_finish(self, gender: str):
        self.builder.button(text='✅ Создать', callback_data=AddCharFinishCall(go=True))
        self.builder.button(text='🔁 Изменить', callback_data=AddCharGenderCall(gender=gender, to_change=True))
        return self.builder.adjust(1).as_markup()

class InfoCharIKB(BotIKB):
    def get_list(self, main_char_id: int | None, char_dict: dict[int, str]):
        if main_char_id in char_dict:
            main_char = char_dict.pop(main_char_id)
            self.builder.button(text=f'👑 {main_char}', callback_data=InfoCharListCall(char_id=main_char_id, main=True))
        for char_id, char_name in char_dict.items():
            self.builder.button(text=f'♟️ {char_name}', callback_data=InfoCharListCall(char_id=char_id))
        return self.builder.adjust(1).as_markup()
            
    def chouse_main_char(self, char_id: int, main: bool = False): 
        self.builder.button(text='↩️ Назад', callback_data=InfoCharChooseCall(back=True))
        if main == False:
            self.builder.button(text='🕹️ Выбрать', callback_data=InfoCharChooseCall(char_id=char_id))   
        return self.builder.adjust(2).as_markup()

    @property
    def add_char(self):
        return AddCharIKB()

class InventoryIKB(BotIKB):
    def back(self, where: str, item_id: int | None = None):
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id))
        return self.builder.adjust(1).as_markup()
    
    def items(self, items: dict[int, ItemDB]):
        for id, item in items.items():
            self.builder.button(text=f'{item.sketch.emodzi} {item.sketch.name} {f'({item.quantity}шт.)' if item.quantity > 1 else ''}', callback_data=InventoryItemsCall(item=id))
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsActionCall(to_pick_up=True))
        return self.builder.adjust(1).as_markup()
    
    def throw(self, where: str):
        self.builder.button(text='🚮 Выбросить', callback_data=InventoryItemsActionCall(to_throw=True))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def look(self):
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsActionCall(to_pick_up=True))
        return self.builder.adjust(2).as_markup()
    
    def location_items(self, items: list[ItemDB], where: str, back_where: str):
        for item in items:
            self.builder.button(text=f'{item.sketch.emodzi} {item.sketch.name} {f'({item.quantity}шт.)' if item.quantity > 1 else ''}', callback_data=InventoryItemsPickUpCall(item_id=item.id))
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsGoCall(where=where))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=back_where))
        return self.builder.adjust(1).as_markup() 

    def pick_up(self, item_id: int, where: str):
        self.builder.button(text='🫳 Поднять', callback_data=InventoryItemsPickUpCall(item_id=item_id, to_pick_up=True))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(item_id=item_id, where=where))
        return self.builder.adjust(1).as_markup()            
    