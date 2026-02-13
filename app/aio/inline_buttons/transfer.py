from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.db.models.item import ItemSketchDB, ItemDB
from app.db.models.char import CharacterDB
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.callback.transfer import (ItemTransferCharIdCall, 
                                           ItemTransferChoiseCharCall, 
                                           ItemTransferStatusEnum, 
                                           ItemTransferTradeStatusCall, 
                                           ItemTransferActionCall, 
                                           ItemTransferStartCall, 
                                           ItemTransferBackCall, 
                                           ItemTransferCharPageCall, 
                                           ItemTransferItemIdCall,
                                           ItemTransferItemPageCall)
from app.enum_type.transfer import ItemTransferStatusEnum

class ItemTransferIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=ItemTransferBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def new_transfer(self):
        self.builder.button(text='🔄️ Обмен', callback_data=ItemTransferStartCall(to_trade=True))
        return self.builder.adjust(1).as_markup()

    def choise_char(self, where: str):
        self.builder.button(text='📋 Из списка ближайших', callback_data=ItemTransferChoiseCharCall(to_list=True))
        self.builder.button(text='🔎 Через поиск', callback_data=ItemTransferChoiseCharCall(to_search=True))
        self.builder.button(text='↩️ Назад', callback_data=ItemTransferBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def charpage(self, chars: list[CharacterDB], page: int, max_page: int, where: str):
        for char in chars:
            self.builder.button(text=f'💠 {char.exist.full_name}', callback_data=ItemTransferCharIdCall(char_id=char.id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ItemTransferCharPageCall(page=page-1).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ItemTransferCharPageCall(page=page+1).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ItemTransferBackCall(where=where).pack()))
        return self.builder.as_markup()      
    
    def menu(self, emodzi1: str = '👤', emodzi2: str = '👤'):
        self.builder.button(text=f'{emodzi1}', callback_data=ItemTransferChoiseCharCall(to_my_char=True))
        self.builder.button(text='➕', callback_data=ItemTransferActionCall(action='+', side=1)) 
        self.builder.button(text='➖', callback_data=ItemTransferActionCall(action='-', side=1))
        self.builder.button(text=f'{emodzi2}', callback_data=ItemTransferStartCall(to_trade=True))        
        self.builder.button(text='➕', callback_data=ItemTransferActionCall(action='+', side=2)) 
        self.builder.button(text='➖', callback_data=ItemTransferActionCall(action='-', side=2))       
        self.builder.button(text='📨 Отправить', callback_data=ItemTransferTradeStatusCall(status=ItemTransferStatusEnum.PENDING.value))   
        return self.builder.adjust(3, 3, 1).as_markup()
  
    def itempage(self, datas: list[ItemSketchDB], page: int, max_page: int, where: str, side: int):
        for data in datas:
            self.builder.button(text=f'{data.emodzi} {data.name} [{data.id}]', callback_data=ItemTransferItemIdCall(item_id=data.id, side=side))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=ItemTransferItemPageCall(page=page-1, side=side).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=ItemTransferItemPageCall(page=page+1, side=side).pack()))
        if len(pages) > 0:
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=ItemTransferBackCall(where=where).pack()))
        return self.builder.as_markup()

