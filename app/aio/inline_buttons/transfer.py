from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.db.models.item import ItemSketchDB, ItemDB
from app.db.models.char import CharacterDB
from app.db.models.transfer import TransferDB
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.aio.cls.callback.transfer import (ItemTransferCharIdCall, 
                                           ItemTransferChoiseCharCall,
                                           ItemTransferTradeStatusCall, 
                                           ItemTransferActionCall, 
                                           ItemTransferStartCall, 
                                           ItemTransferBackCall, 
                                           ItemTransferCharPageCall, 
                                           ItemTransferItemIdCall,
                                           ItemTransferItemPageCall,
                                           InfoTransferInfoCall,
                                           InfoTransferBackCall,
                                           InfoTransferPageCall,
                                           InfoTransferStartCall,
                                           InfoTransferStatusCall,
                                           InfoTransferSortedCall,
                                           InfoTransferActionCall,
                                           InfoTransferSearchCall)
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
        self.builder.button(text='📨 Отправить', callback_data=ItemTransferTradeStatusCall(status=ItemTransferStatusEnum.CONFIRMED.value))
        self.builder.button(text='💾 Сохранить в черновик', callback_data=ItemTransferTradeStatusCall(status=ItemTransferStatusEnum.CREATED.value))
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

class InfoTransferIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=InfoTransferBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def menu(self):
        self.builder.button(text='📝 Черновики', callback_data=InfoTransferSortedCall(status='created'))
        self.builder.button(text='⌛ Отправленные', callback_data=InfoTransferSortedCall(status='confirmed'))
        self.builder.button(text='📩 Полученные', callback_data=InfoTransferSortedCall(status='received'))
        self.builder.button(text='✅ Завершенные', callback_data=InfoTransferSortedCall(status='completed'))
        self.builder.button(text='❌ Отклоненные', callback_data=InfoTransferSortedCall(status='rejected'))
        self.builder.button(text='🔎 Поиск по ID', callback_data=InfoTransferSearchCall(search_type='transfer_id'))
        self.builder.button(text='🔎 Поиск по Персонажу', callback_data=InfoTransferSearchCall(search_type='char_id'))
        self.builder.button(text='🔎 Поиск по Предмету', callback_data=InfoTransferSearchCall(search_type='item_id'))
        self.builder.button(text='➕ Создать', callback_data=InfoTransferStartCall(to_create=True))
        #self.builder.button(text='ℹ️ FAQ', callback_data=InfoTransferStartCall(to_faq=True))
        return self.builder.adjust(1, 2, 2, 2, 1, 1, 1).as_markup()

    def pages(self, my_char_id: int, transfers: list[TransferDB], page: int, max_page: int, where: str):
        for transfer in transfers:
            self.builder.button(text=("📥" if transfer.seller.id != my_char_id else "📤") +
                                f' {transfer.seller.exist.full_name if transfer.seller.id != my_char_id else transfer.buyer.exist.full_name} [id:{transfer.id}]', 
                                callback_data=InfoTransferInfoCall(transfer_id=transfer.id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=InfoTransferPageCall(page=page-1).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=InfoTransferPageCall(page=page+1).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=InfoTransferBackCall(where=where).pack()))
            
        return self.builder.as_markup()   

    def to_create(self, transfer_id: int, where: str):
        self.builder.button(text='🗑️ Удалить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_delete=True))
        self.builder.button(text='📨 Отправить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_new_status=True, new_status='confirmed'))
        #self.builder.button(text='✒️ Изменить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_redact=True))
        self.builder.button(text='↩️ Назад', callback_data=InfoTransferBackCall(where=where))
        return self.builder.adjust(2).as_markup()

    def to_complete(self, transfer_id: int, where: str):
        self.builder.button(text='✅ Принять', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_complete=True, new_status='completed'))
        self.builder.button(text='❌ Отклонить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_new_status=True, new_status='rejected'))
        #self.builder.button(text='✒️ Изменить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_redact=True))
        self.builder.button(text='↩️ Назад', callback_data=InfoTransferBackCall(where=where))
        return self.builder.adjust(2, 1).as_markup()   

    def to_confirm(self, transfer_id: int, where: str):
        self.builder.button(text='❌ Отозвать', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_new_status=True, new_status='rejected'))
        #self.builder.button(text='✒️ Изменить', callback_data=InfoTransferActionCall(transfer_id=transfer_id, to_redact=True))
        self.builder.button(text='↩️ Назад', callback_data=InfoTransferBackCall(where=where))
        return self.builder.adjust(1).as_markup()   
    

    