from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.aio.cls.callback.craft import CraftBackCall, CraftIdCall, CraftPageCall, CraftActionCall, CraftActionHidenCall
from app.db.models.item import CraftDB
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class CraftIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=CraftBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def crafts(self, crafts: list[CraftDB], page: int, max_page: int):
        for craft in crafts:
            self.builder.button(text=f'{craft.ingredients_emodzi(to_str=True)} -> {craft.results_emodzi(to_str=True)}', callback_data=CraftIdCall(craft_id=craft.id))
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
    
    def craft_hiden(self, where: str):
        self.builder.button(text=f'💮 Ингредиенты', callback_data=CraftActionCall(to_faq_ingredient=True))
        self.builder.button(text='➕', callback_data=CraftActionHidenCall(action='+', item_type='ingredient')) 
        self.builder.button(text='➖', callback_data=CraftActionHidenCall(action='-', item_type='ingredient'))
        self.builder.button(text=f'🛠️ Инструменты', callback_data=CraftActionCall(to_faq_tool=True))        
        self.builder.button(text='➕', callback_data=CraftActionHidenCall(action='+', item_type='tools')) 
        self.builder.button(text='➖', callback_data=CraftActionHidenCall(action='-', item_type='tools'))       
        self.builder.button(text='✅ Скрафтить', callback_data=CraftActionCall(to_craft=True))
        self.builder.button(text='↩️ Назад', callback_data=CraftBackCall(where=where))        
        return self.builder.adjust(3, 3, 1).as_markup()   
    
