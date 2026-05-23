from app.aio.cls.callback.action import (ActionBackCall, 
                                         MenuCall, 
                                         ActionCall, 
                                         ActionRedactCall, 
                                         LookAroundCall, 
                                         ActionPageCall, 
                                         ThrowItemCall, 
                                         ThrowItemQuantityCall, 
                                         PaperCall,
                                         BookCall,
                                         BookSettingCall,
                                         RadioCall)
from app.aio.cls.callback.faq import FAQCall
from app.aio.cls.callback.char import InventoryItemsGoCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.enum_type.tags import ActionTags
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.logic.actions import ActionBase
from app.db.models.char import ExistenceDB, ItemDB, CharacterDB
from app.db.models.main import UserDB

class ActionIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where=where, is_details=True, tg_id=self.tg_id)).as_markup()

    def actions(self, actions: dict[str, list], is_details: bool = True):
        for tag, text in actions.items():
            self.builder.button(text=(' '.join(text) if not(is_details) else text[0]), callback_data=ActionCall(tag=tag, tg_id=self.tg_id))
        self.builder.adjust((3 if is_details else 1), repeat=True)
        self.builder.row(InlineKeyboardButton(text=('➖ Менее подробнее' if not(is_details) else '➕ Подробнее'), callback_data=ActionBackCall(where='actions', is_details=not(is_details), tg_id=self.tg_id).pack()))
        return self.builder.as_markup()
 




    def wake_up(self):        
        self.builder.button(text='📊 Статистика', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='🌞 Проснуться', callback_data=ActionCall(tag=ActionTags.wake_up, tg_id=self.tg_id))
        return self.builder.as_markup()

    def stop(self):
        self.builder.button(text='📊 Статистика', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='⏸️ Остановиться', callback_data=ActionCall(tag=ActionTags.stop, tg_id=self.tg_id))
        return self.builder.as_markup()

    def stats(self):
        self.builder.button(text='🔁 Обновить', callback_data=ActionRedactCall(tag=ActionTags.stats, to_stats=True, tg_id=self.tg_id))
        self.builder.button(text='⏸️ Остановиться', callback_data=ActionCall(tag=ActionTags.stop, tg_id=self.tg_id))
        return self.builder.as_markup()    
      




    def redact(self, tag: str, emodzi: str, action_text: str, where: str, item_id: int, minute: int | None = None, items: dict[str, ItemDB | None] | None = None, char_id: int | None = None):      
        self.builder.button(text=('⏱️ Изменить время' if minute and minute > 0 else '➕ Добавить таймер'), callback_data=ActionRedactCall(tag=tag, to_time=True, tg_id=self.tg_id))
        if minute and minute > 0:
            self.builder.button(text='❌ Отключить таймер', callback_data=ActionRedactCall(tag=tag, to_del_timer=True, tg_id=self.tg_id))
        if items:
            for item_tag, item in items.items():
                self.builder.button(text=item.sketch.text if item else '❌ Нету', callback_data=ActionRedactCall(tag=tag, to_item=True, item_tag=item_tag, minute=minute, is_details=True, char_id=char_id, tg_id=self.tg_id))
        self.builder.adjust(*[1, 1, 2] if minute and minute > 0 else [1, 2])
        self.builder.row(
            InlineKeyboardButton(text='↩️ Назад', callback_data=ActionBackCall(where=where, is_details=True, tg_id=self.tg_id).pack()),   
            InlineKeyboardButton(text=emodzi + ' ' + action_text, callback_data=ActionCall(tag=tag, step=2, minute=minute, item_id=item_id, tg_id=self.tg_id).pack()), 
            width=2)
        return self.builder.as_markup()

    def use_items(self, tag: str, minute: int, items: list[ItemDB] | None):   
        if items:
            for item in items:
                self.builder.button(**item.button_text, callback_data=ActionCall(tag=tag, step=1, minute=minute, item_id=item.id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ActionCall(tag=tag, step=1, minute=minute, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()



    def lookaround(self, results: list[tuple[ExistenceDB | None, ActionBase | None]]):        
        for exist, action in results:
            self.builder.button(text=f'{action.emodzi} {exist.full_name} {action.action_text}', callback_data=LookAroundCall(tg_id=self.tg_id))
        self.builder.button(text='👁️ Посмотреть ещё раз', callback_data=ActionCall(tag=ActionTags.lookaround, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where='actions', is_details=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()




    def item_throw(self, char: CharacterDB, kwargs: dict = {}, where: str | None = None):
        print(kwargs)
        for item in char.exist.inventory.items:
            self.builder.button(text=item.text, callback_data=ThrowItemCall(tag=ActionTags.throw, **(kwargs | {'item_id': item.id, 'quantity':1}), tg_id=self.tg_id))
        if where:
            self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where='actions', is_details=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()     

    def char_throw(self, chars: list[CharacterDB], kwargs: dict = {}, page: int = 0, max_page: int = 0, where: str | None = None):
        for char in chars:
            self.builder.button(text=f'💠 {char.exist.full_name}', callback_data=ThrowItemCall(tag=ActionTags.throw, **(kwargs | {'purpose_char_id': char.id}), tg_id=self.tg_id))
        self.builder.adjust(2)
        arrows_page = []
        if page > 0:
            arrows_page.append(InlineKeyboardButton(text='⬅️', callback_data=ActionPageCall(page=page-1, tag=ActionTags.throw, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            arrows_page.append(InlineKeyboardButton(text='➡️', callback_data=ActionPageCall(page=page+1, tag=ActionTags.throw, tg_id=self.tg_id).pack()))
            
        if len(arrows_page) > 0: 
            self.builder.row(*arrows_page)
        self.builder.row(InlineKeyboardButton(text='↩️ Назад', callback_data=ActionBackCall(where='actions', is_details=True, tg_id=self.tg_id).pack()))
            
        return self.builder.as_markup() 

    def throw_menu(self, kwargs: dict = {}, where: str = 'actions'):
        self.builder.button(text='🥏 Кинуть', callback_data=ThrowItemCall(tag=ActionTags.throw, step=2, **kwargs, tg_id=self.tg_id))
        self.builder.button(text='✏️ Изменить количество', callback_data=ThrowItemQuantityCall(tag=ActionTags.throw, **kwargs, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=ActionBackCall(where=where, is_details=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()     
 



    def dice(self, kwargs: dict = {}):
        self.builder.button(text='🥏 Перебросить', callback_data=ActionCall(tag=ActionTags.dice, **kwargs, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()     
 
    def dice_command(self):
        self.builder.button(text='ℹ️ Помощь', callback_data=FAQCall(faq=ActionTags.dice, tg_id=self.tg_id, to_answer_callback=False))
        self.builder.button(text='❌ Отменить', callback_data=MenuCall(where='cancel', is_details=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()   
 



    def redact_paper(self, item_id: int, is_have_text: bool, is_escape: bool, where: str = 'item'):
        if is_have_text:
            self.builder.button(text='✏️ Изменить надпись', callback_data=PaperCall(tag=ActionTags.paper, item_id=item_id, step=2, tg_id=self.tg_id))
            self.builder.button(text='🗑️ Убрать надпись', callback_data=PaperCall(tag=ActionTags.paper, item_id=item_id, step=4, tg_id=self.tg_id))
            self.builder.button(text='👁️ Показать HTML-теги' if not(is_escape) else '🌫️ Скрыть HTML-теги', callback_data=PaperCall(tag=ActionTags.paper, item_id=item_id, is_escape=not(is_escape), tg_id=self.tg_id))
        else:
            self.builder.button(text='✏️ Добавить надпись', callback_data=PaperCall(tag=ActionTags.paper, item_id=item_id, step=2, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def paper_back(self, item_id: int):
        self.builder.button(text='↩️ Назад', callback_data=ActionCall(tag=ActionTags.paper, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()    
    




    def book(self, item_id: int, page: int, max_page: int, book_info: bool, where: str = 'item'):
        arrow = 0
        if page > 0:
            self.builder.button(text='⬅️', callback_data=BookCall(tag=ActionTags.book, page=page-1, item_id=item_id, tg_id=self.tg_id))
            arrow += 1
        if page != max_page - 1:
            self.builder.button(text='➡️', callback_data=BookCall(tag=ActionTags.book, page=page+1, item_id=item_id, tg_id=self.tg_id))
            arrow += 1
        if max_page > 2:
            self.builder.button(text=f'{page + 1}/{max_page} стр', callback_data=BookCall(tag=ActionTags.book, page=page, step=2, item_id=item_id, tg_id=self.tg_id))
        if book_info:
            self.builder.button(text='➕ Добавить страницу', callback_data=BookCall(tag=ActionTags.book, page=page, step=3, item_id=item_id, tg_id=self.tg_id))
            if max_page > 0:
                self.builder.button(text='➖ Удалить страницу', callback_data=BookCall(tag=ActionTags.book, page=page, step=5, item_id=item_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='✏️ Назвать книгу', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=0, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(arrow or 1, 1).as_markup()

    def book_pages(self, page: int, item_id: int, text_pages: list[str]):
        k = 0
        for text_page in text_pages:
            k += 1
            self.builder.button(text=f'{text_page}... ({k} стр.)', callback_data=BookCall(tag=ActionTags.book, page=page, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=BookCall(tag=ActionTags.book, page=page, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def book_back(self, page: int, item_id: int):
        self.builder.button(text='↩️ Назад', callback_data=BookCall(tag=ActionTags.book, page=page, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()    



    def book_setting(self, item_id: int, is_redact: bool, where: str = 'item'):             
        self.builder.button(text='🏷️ Изменить название', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=0, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='🎭 Изменить псевдоним', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=2, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='📃 Изменить описание', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=3, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='🔏 Запретить редактирование' if is_redact else ' 🔓 Разрешить редактирование', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=4, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='🗑️ Очистить книгу', callback_data=BookSettingCall(tag=ActionTags.book_setting, step=5, item_id=item_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()  

    def book_setting_back(self, item_id: int):
        self.builder.button(text='↩️ Назад', callback_data=BookSettingCall(tag=ActionTags.book_setting, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()    




    def radio(self, item_id: int, micro: bool, swoo: bool, where: str = 'item'): 
        self.builder.button(text='✅ Включить звук' if not swoo else '❌ Отключить звук', callback_data=RadioCall(tag=ActionTags.radio, step=3, micro=micro, swoo=swoo, item_id=item_id, tg_id=self.tg_id))  
        if swoo:
            self.builder.button(text='✅ Включить микрофон' if not micro else '❌ Отключить микрофон', callback_data=RadioCall(tag=ActionTags.radio, step=2, micro=micro, swoo=swoo, item_id=item_id, tg_id=self.tg_id)) 
            self.builder.button(text='🔃 Переключить канал', callback_data=RadioCall(tag=ActionTags.radio, step=4, micro=micro, swoo=swoo, item_id=item_id, tg_id=self.tg_id)) 
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()    
 
    def micro(self, item_id: int):
        self.builder.button(text='❌ Отключить микрофон', callback_data=RadioCall(tag=ActionTags.radio, micro_off=True, item_id=item_id, tg_id=self.tg_id)) 
        return self.builder.adjust(1).as_markup()    
       



    def rename_menu(self, item_id: int, args: str):
        self.builder.button(text='✏️ Другое имя', callback_data=ActionCall(tag=ActionTags.tag, step=1, args=args, item_id=item_id, tg_id=self.tg_id)) 
        self.builder.button(text='✅ Переименовать', callback_data=ActionCall(tag=ActionTags.tag, step=3, args=args, item_id=item_id, tg_id=self.tg_id)) 
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where='item', item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()   
        
 

    def item_back(self, item_id: int, where: str = 'item'):
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()    
    

