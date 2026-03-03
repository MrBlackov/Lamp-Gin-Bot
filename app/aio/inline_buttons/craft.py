from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.aio.cls.callback.craft import (CraftBackCall, 
                                        CraftIdCall, 
                                        CraftPageCall, 
                                        CraftActionCall, 
                                        CraftCreateActionCall,
                                        CraftItemIdCall,
                                        CraftItemPagesCall)
from app.db.models.item import CraftDB, ItemSketchDB
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AddCraftIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=CraftBackCall(where=where))
        return self.builder.adjust(1).as_markup()

    def new_craft(self, is_admin: bool):
        self.builder.button(text=f'💮 Ингредиенты', callback_data=CraftActionCall(to_faq=True, faq='ingredients'))
        self.builder.button(text='➕', callback_data=CraftCreateActionCall(action='+', item_type='ingredients')) 
        self.builder.button(text='➖', callback_data=CraftCreateActionCall(action='-', item_type='ingredients'))
        self.builder.button(text=f'🛠️ Инструменты', callback_data=CraftActionCall(to_faq=True, faq='tools'))        
        self.builder.button(text='➕', callback_data=CraftCreateActionCall(action='+', item_type='tools')) 
        self.builder.button(text='➖', callback_data=CraftCreateActionCall(action='-', item_type='tools'))       
        self.builder.button(text=f'⚗️ Результат', callback_data=CraftActionCall(to_faq=True, faq='results'))        
        self.builder.button(text='➕', callback_data=CraftCreateActionCall(action='+', item_type='results')) 
        self.builder.button(text='➖', callback_data=CraftCreateActionCall(action='-', item_type='results'))  
        self.builder.button(text='⏱️ Время крафта', callback_data=CraftActionCall(to_time=True)) 
        self.builder.button(text='📨 Отправить крафт', callback_data=CraftActionCall(to_send=True))  
        if is_admin:    
            self.builder.button(text='✅ Создать крафт', callback_data=CraftActionCall(to_craft=True))       
        return self.builder.adjust(3, 3, 3, 1).as_markup()   

    def itempage(self, datas: list[ItemSketchDB], page: int, max_page: int, where: str, item_type: str):
        for data in datas:
            self.builder.button(text=f'{data.emodzi} {data.name} [{data.id}]', callback_data=CraftItemIdCall(item_id=data.id, item_type=item_type))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=CraftItemPagesCall(page=page-1, item_type=item_type).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=CraftItemPagesCall(page=page+1, item_type=item_type).pack()))
        if len(pages) > 0:
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=CraftBackCall(where=where).pack()))
        return self.builder.as_markup()

class CraftIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=CraftBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def crafts(self, crafts: list[CraftDB], page: int, max_page: int):
        for craft in crafts:
            if len(craft.ingredients) == 1 and len(craft.results) == 1:
                text = f'{craft.ingredients_emodzi(to_str=True)} {craft.ingredient_text()} >>> {craft.results_emodzi(to_str=True)} {craft.result_text()}'
            elif len(craft.ingredients) > 1:
                text = f'{craft.ingredients_emodzi(to_str=True)} >>> {craft.results_emodzi(to_str=True)} {craft.result_text()}'
            elif len(craft.results) > 1:
                text = f'{craft.ingredients_emodzi(to_str=True)} {craft.ingredient_text()} >>> {craft.results_emodzi(to_str=True)}'
            else:
                text = f'{craft.ingredients_emodzi(to_str=True)} >>> {craft.results_emodzi(to_str=True)}'
            
            self.builder.button(text=text, callback_data=CraftIdCall(craft_id=craft.id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=CraftPageCall(page=page-1).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=CraftPageCall(page=page+1).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        #self.builder.row(InlineKeyboardButton(text='🧪 Попробовать самому', callback_data=CraftActionCall(to_craft_hiden=True).pack()))
        return self.builder.as_markup()

    def craft(self, where: str):
        self.builder.button(text='🛠️ Скрафтить', callback_data=CraftActionCall(to_craft=True))
        self.builder.button(text='↩️ Назад', callback_data=CraftBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
