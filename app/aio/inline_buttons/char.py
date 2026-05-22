from app.aio.cls.callback.char import (
                                       AddCharGenderCall,  
                                       AddCharNameCall, 
                                       AddCharQueryNameCall, 
                                       AddCharRandomNameCall,
                                       AddCharSketchCall,
                                       AddCharDescriptCall,
                                       AddCharFinishCall,
                                       InfoCharListCall, 
                                       InfoCharDeleteCall,
                                       InfoCharChooseCall,
                                       InventoryItemsCall,
                                       InventoryItemsGoCall, 
                                       InventoryItemsActionCall,
                                       InventoryItemsPickUpCall,
                                       MenuCall,
                                       NewCharBackCall,
                                       NewCharBonusCall,
                                       NewCharGenderCall,
                                       NewCharActionCall,
                                       NewCharNameActionCall,
                                       NewCharNameCall,
                                       NewCharPageNameCall,
                                       NewCharPageSkillCall,
                                       NewCharSkillCall,
                                       )
from app.aio.cls.callback.faq import FAQCall
from app.aio.cls.callback.action import ActionCall, ThrowItemCall
from app.db.models.item import ItemDB, SkillDB, SkillSketchDB
from app.db.models.char import CharacterDB
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.logic.actions import ActionSelf

class NewCharIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def chouse_gender(self):
        self.builder.button(text='👨 Мужской', callback_data=NewCharGenderCall(gender='M', tg_id=self.tg_id))
        self.builder.button(text='👩 Женский', callback_data=NewCharGenderCall(gender='W', tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()
    
    def get_bonus_char(self, url: str):
        self.builder.button(text='➕ Подписаться', url=url)
        self.builder.button(text='✅ Проверить', callback_data=NewCharBonusCall(tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def actions(self):
        self.builder.button(text='♠️ Имя', callback_data=NewCharActionCall(to_rename=True, name_type='first', tg_id=self.tg_id))
        self.builder.button(text='♣️ Фаимилия', callback_data=NewCharActionCall(to_rename=True, name_type='last', tg_id=self.tg_id))
        self.builder.button(text='💡 Навыки', callback_data=NewCharActionCall(to_skills=True, tg_id=self.tg_id))
        #self.builder.button(text='🎲 Перегенерировать', callback_data=NewCharActionCall(to_generate=True, tg_id=self.tg_id))
        self.builder.button(text='📝 Описание', callback_data=NewCharActionCall(to_description=True, tg_id=self.tg_id))
        self.builder.button(text='✅ Создать', callback_data=NewCharActionCall(to_create=True, tg_id=self.tg_id))
        self.builder.button(text='❓ Помощь', callback_data=FAQCall(faq='new_char', tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where='gender', tg_id=self.tg_id))
        return self.builder.adjust(2, 2, 1, 1, 1).as_markup()

    def redact_skills(self, skills: list[SkillDB], where: str):
        for skill in skills:
            if skill.sketch.is_hide:
                continue
            if skill.sketch.custom_emodzi_id:
                text = f' {skill.sketch.name} - {skill.level} ур.'
                custom_emodzi_id = skill.sketch.custom_emodzi_id
            else:
                text = f'{skill.sketch.emodzi} {skill.sketch.name} - {skill.level} ур.'
                custom_emodzi_id = None
            self.builder.button(text=text, custom_emodzi_id=custom_emodzi_id, callback_data=NewCharSkillCall(skill_tag=skill.sketch.tag, is_base=skill.sketch.is_base, level=skill.level, tg_id=self.tg_id))
        self.builder.button(text='➕ Добавить', callback_data=NewCharActionCall(to_add_skills=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()        

    def skills(self, skills: list[SkillSketchDB], page: int, max_page: int, where: str):
        for skill in skills:
            if skill.is_hide:
                continue
            if skill.custom_emodzi_id:
                button_text = {'text':  f' {skill.name} - {skill.price} 💮', 'icon_custom_emoji_id': skill.custom_emodzi_id}
            else:
                button_text = {'text': f'{skill.emodzi} {skill.name} - {skill.price} 💮'}
            self.builder.button(**button_text, callback_data=NewCharSkillCall(skill_tag=skill.tag, is_base=skill.is_base, level=1, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=NewCharPageSkillCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=NewCharPageSkillCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()        

    def redact_skill_level(self, skill_tag: str, level: int, is_base: bool, where: str):
        self.builder.button(text='➕', callback_data=NewCharSkillCall(skill_tag=skill_tag, level=level+1, is_base=is_base, tg_id=self.tg_id))
        if level > 0:
            self.builder.button(text='➖', callback_data=NewCharSkillCall(skill_tag=skill_tag, level=level-1, is_base=is_base, tg_id=self.tg_id))  
            adjust = [2, 1]
        else:
            adjust = [1]
        self.builder.button(text='✅ Применить', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))      
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(*adjust).as_markup()        

    def redact_name(self, name_type: str, where: str):
        self.builder.button(text='🔎 Поиск', callback_data=NewCharNameActionCall(to_query=True, name_type=name_type, tg_id=self.tg_id))
        self.builder.button(text='🎲 Рандом', callback_data=NewCharNameActionCall(to_random=True, name_type=name_type, tg_id=self.tg_id))   
        if name_type == 'last':
            self.builder.button(text='❌ Убрать', callback_data=NewCharNameActionCall(to_delete=True, name_type='last', tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()      
    
    def random_name(self, name: str, name_type: str, where: str):
        self.builder.button(text='🔁 Другое', callback_data=NewCharNameActionCall(to_random=True, name_type=name_type, tg_id=self.tg_id))
        self.builder.button(text='✅ Применить', callback_data=NewCharNameCall(name=name, name_type=name_type, tg_id=self.tg_id))     
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()  

    def names(self, names: list[str], name_type: str, page: int, max_page: int, where: str):
        for name in names:
            self.builder.button(text=name.title(), callback_data=NewCharNameCall(name=name.title(), name_type=name_type, tg_id=self.tg_id))
        self.builder.adjust(2)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=NewCharPageNameCall(page=page-1, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=NewCharPageNameCall(page=page+1, tg_id=self.tg_id).pack()))
        if len(pages) > 0: 
            self.builder.row(*pages)
        if where:
            self.builder.row(InlineKeyboardButton(text='↩️', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id).pack()))
        return self.builder.as_markup()        

    def finish(self, where: str):
        self.builder.button(text='✅ Согласиться', callback_data=NewCharActionCall(to_create=True, is_finished=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewCharBackCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()


class AddCharIKB(BotIKB):
    def query_back(self, first_name: bool = True):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='↩️ Назад', callback_data=AddCharQueryNameCall(back=True, first_name=first_name, tg_id=self.tg_id).pack())]])

    def chouse_gender(self, to_change: bool = False):
        self.builder.button(text='👨 Мужской', callback_data=AddCharGenderCall(gender='M', to_change=to_change, tg_id=self.tg_id))
        self.builder.button(text='👩 Женский', callback_data=AddCharGenderCall(gender='W', to_change=to_change, tg_id=self.tg_id))
        self.builder.adjust(2)
        return self.builder.as_markup()
    
    def get_bonus_char(self, url: str):
        self.builder.button(text='➕ Подписаться', url=url)
        self.builder.button(text='✅ Проверить', callback_data=AddCharNameCall(get_bonus=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def chouse_regim_name(self, first_name: bool = True):
        self.builder.button(text='🔍 Поищем', callback_data=AddCharNameCall(regim='query', first_name=first_name, tg_id=self.tg_id))
        self.builder.button(text='🎲 Случайно', callback_data=AddCharNameCall(regim='random', first_name=first_name, tg_id=self.tg_id))
        if not first_name: 
            self.builder.button(text='Пропустить', callback_data=AddCharNameCall(first_name=False, to_pass=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=AddCharNameCall(back=True, first_name=first_name, tg_id=self.tg_id))
        self.builder.adjust(2, 1)
        return self.builder.as_markup()
    
    def get_pages_names(self, texts: list[str], page: int, max_page: int = 1, first_name: bool = True):
        for text in texts:
            self.builder.button(text=text, callback_data=AddCharQueryNameCall(name=text, first_name=first_name, tg_id=self.tg_id))
        self.builder.adjust(*[2 for _ in range(len(texts))])
        arrows_page = []
        if page > 0:
            arrows_page.append(InlineKeyboardButton(text='⬅️', callback_data=AddCharQueryNameCall(page=page-1, next_page=True, first_name=first_name, tg_id=self.tg_id).pack()))
        if page != max_page - 1:
            arrows_page.append(InlineKeyboardButton(text='➡️', callback_data=AddCharQueryNameCall(page=page+1, next_page=True, first_name=first_name, tg_id=self.tg_id).pack()))
            
        if len(arrows_page) > 0: 
            self.builder.row(*arrows_page)
        self.builder.row(InlineKeyboardButton(text='↩️', callback_data=AddCharQueryNameCall(back=True, first_name=first_name, tg_id=self.tg_id).pack()))
            
        return self.builder.as_markup()        
        
    def get_rnd_name(self, name: str, first_name: bool = True):
        self.builder.button(text='↩️', callback_data=AddCharRandomNameCall(back=True, first_name=first_name, tg_id=self.tg_id))
        self.builder.button(text='🔄️', callback_data=AddCharRandomNameCall(regeneration=True, first_name=first_name, tg_id=self.tg_id))
        self.builder.button(text='✅', callback_data=AddCharRandomNameCall(name=name, first_name=first_name, tg_id=self.tg_id))
        self.builder.adjust(3)
        return self.builder.as_markup()

    def get_sketchs(self, sketch_id: int, max_quantity: int):
        max_quantity -= 1
        self.builder.button(text='↩️', callback_data=AddCharSketchCall(id=sketch_id, back=True, tg_id=self.tg_id))
        if sketch_id < max_quantity:
            free_quantity = max_quantity - sketch_id
            self.builder.button(text=f'{free_quantity} 🔄️', callback_data=AddCharSketchCall(id=sketch_id, another=True, tg_id=self.tg_id))
        self.builder.button(text='✅', callback_data=AddCharSketchCall(id=sketch_id, another=False, tg_id=self.tg_id))
        self.builder.adjust(3)
        return self.builder.as_markup()       

    def descript(self):
        self.builder.button(text='➡️ Пропустить', callback_data=AddCharDescriptCall(to_pass=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=AddCharDescriptCall(back=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
        
    def to_finish(self, gender: str):
        self.builder.button(text='✅ Создать', callback_data=AddCharFinishCall(go=True, tg_id=self.tg_id))
        self.builder.button(text='🔁 Изменить', callback_data=AddCharGenderCall(gender=gender, to_change=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

class InfoCharIKB(BotIKB):
    def get_list(self, main_char_id: int | None, char_dict: dict[int, CharacterDB]):
        die_chars = []
        if main_char_id in char_dict:
            main_char = char_dict.pop(main_char_id)
            self.builder.button(text=f'👑 {main_char.exist.full_name}', callback_data=InfoCharListCall(char_id=main_char_id, main=True, tg_id=self.tg_id))
        for char_id, char in char_dict.items():
            if char.exist.die:
                die_chars.append(char)
                continue
            self.builder.button(text=f'♟️ {char.exist.full_name}', callback_data=InfoCharListCall(char_id=char_id, tg_id=self.tg_id))
        for char in die_chars:
            self.builder.button(text=f'☠️ {char.exist.full_name}', callback_data=InfoCharListCall(char_id=char.id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
            
    def chouse_main_char(self, char_id: int, exist_id: int, main: bool = False, is_die: bool = False):  
        adjust = [1]
        if main == False and is_die == False:
            self.builder.button(text='🕹️ Выбрать', callback_data=InfoCharChooseCall(char_id=char_id, tg_id=self.tg_id)) 
        if main:
            self.builder.button(text='💼 Инвентарь', callback_data=MenuCall(where='inventory', tg_id=self.tg_id)) 
            self.builder.button(text='⚗️ Крафты', callback_data=MenuCall(where='crafts', tg_id=self.tg_id)) 
            self.builder.button(text='💡 Навыки', callback_data=MenuCall(where='myskills', tg_id=self.tg_id)) 
            self.builder.button(text='🎮 Доействия', callback_data=MenuCall(where='actions', tg_id=self.tg_id)) 
            self.builder.button(text='✉️ Сделки', callback_data=MenuCall(where='transfers', tg_id=self.tg_id)) 
            self.builder.button(text='⚙️ Настройки персонажа', callback_data=MenuCall(where='char_setting', tg_id=self.tg_id))
            adjust = [2, 2, 1]
        if is_die == False:  
            self.builder.button(text='☠️ Повеситься', callback_data=InfoCharDeleteCall(char_id=char_id, exist_id=exist_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InfoCharChooseCall(back=True, tg_id=self.tg_id)) 
        return self.builder.adjust(*adjust).as_markup()
    
    def to_delete_char(self, char_id: int, exist_id: int):
        self.builder.button(text='❌ Нет', callback_data=InfoCharDeleteCall(char_id=char_id, back=True, tg_id=self.tg_id)) 
        self.builder.button(text='✅ Да', callback_data=InfoCharDeleteCall(char_id=char_id, exist_id=exist_id, is_delete=True, tg_id=self.tg_id))  
        return self.builder.adjust(2).as_markup()

    @property
    def add_char(self):
        return AddCharIKB(self.tg_id)

class InventoryIKB(BotIKB):
    def back(self, where: str, item_id: int | None = None):
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, item_id=item_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def items(self, items: dict[int, ItemDB]):
        for id, item in items.items():
            self.builder.button(text=item.text, callback_data=InventoryItemsCall(item=id, tg_id=self.tg_id))
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsActionCall(to_pick_up=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def action(self, item: ItemDB, where: str):
        if item.sketch.action and len(item.sketch.action) > 0:
            for item_action in item.sketch.action:
                action = ActionSelf.item_action().get(item_action)
                if action and action.to_item_button and action.tag != ActionSelf.tags.throw:
                    self.builder.button(text=action.text(), callback_data=ActionCall(tag=action.tag, item_id=item.id, tg_id=self.tg_id))
        self.builder.button(text='🥏 Кинуть', callback_data=ThrowItemCall(tag=ActionSelf.tags.throw, item_id=item.id, tg_id=self.tg_id))  
        self.builder.button(text='🚮 Выбросить', callback_data=InventoryItemsActionCall(to_throw=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def look(self):
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsActionCall(to_pick_up=True, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()
    
    def location_items(self, items: list[ItemDB], where: str, back_where: str):
        for item in items:
            self.builder.button(text=f'{item.sketch.emodzi} {item.sketch.name} {f'({item.quantity}шт.)' if item.quantity > 1 else ''}', callback_data=InventoryItemsPickUpCall(item_id=item.id, tg_id=self.tg_id))
        self.builder.button(text='🕵️ Осмотреться', callback_data=InventoryItemsGoCall(where=where, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(where=back_where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup() 

    def pick_up(self, item_id: int, where: str):
        self.builder.button(text='🫳 Поднять', callback_data=InventoryItemsPickUpCall(item_id=item_id, to_pick_up=True, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=InventoryItemsGoCall(item_id=item_id, where=where, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()            
    