from typing import Literal
from app.db.models.char import CharSettingDB, UserSettingDB

DEFAULT = object()

class SettingValueBase:
    tag: str
    name: str 
    emodzi: str 
    default_value_type = None
    default_value = None
    type: Literal['user', 'char']
    is_bot_default: bool = False
    is_user_default: bool = False
    redact_values: list = [True, False, DEFAULT]
    description = None
    
    def __init__(self, setting: CharSettingDB | UserSettingDB | None = None):
        self.setting = setting
        if setting:
            self.value = setting.settings.get(self.tag)
            if self.value == None and type(setting) == CharSettingDB:
                self.value = setting.user_setting.settings.get(self.tag)
                self.is_user_default = True
            if self.value == None:
                self.value = self.default_value
                self.is_user_default = False
                self.is_bot_default = True
            
            if type(setting) == CharSettingDB: 
                self.default_value = setting.user_setting.settings.get(self.tag) or self.default_value
        else:
            self.value = self.default_value
            self.is_bot_default = True
        
    @classmethod
    def text(self):
        return f'{self.emodzi} {self.name}'
    
    @property
    def button_text(self):
        str_values = {
            'all':'Все',
            'friends':'Только друзья',
            'none':'Никто',
        }
        d = f' (d.{'b.' if self.is_bot_default else 'u.'})' if self.is_bot_default or self.is_user_default else ''
        if type(self.value) == bool:
            return f'{self.text()}: {('✅' if self.value else '❌')}' + d
        if type(self.value) == str:
            return f'{self.text()}: {str_values.get(self.value)}' + d
        return f'{self.text()}: {self.value}' + d

    def redact(self):
        x = self.redact_values.index(self.value) + 1
        if self.is_bot_default or self.is_user_default or x >= len(self.redact_values):
            return self.redact_values[0]
        return self.redact_values[x]
    
    @classmethod
    def faq(self):
        return self.text() + ' - ' + self.description if self.description else None

class is_receive_news(SettingValueBase):
    tag = 'is_receive_news'
    name = 'Получение новостей'
    emodzi = '📢'
    default_value = True
    default_value_type = bool
    description = 'получать новости от разработчика'

class is_receive_friedship_requests(SettingValueBase):
    tag = 'is_receive_friedship_requests'
    name = 'Получение запросов дружбы'
    emodzi = '📧'
    default_value = True
    default_value_type = bool
    description = 'получать запросы для добавления в друзья'
    

class is_hide_in_top(SettingValueBase):
    tag = 'is_hide_in_top'
    name = 'Скрытие имени персонажа в топе'
    emodzi = '😶‍🌫️'
    default_value = False
    default_value_type = bool
    description = 'в топах имя персонажа или имена персонажей будут заменены на "?" '

class is_hide_char(SettingValueBase):
    tag = 'is_hide_char'
    name = 'Скрыть персонажа'
    emodzi = '😶‍🌫️'
    default_value = True
    default_value_type = bool
    description = 'скрывать персоанжа или персонажей от других'
    
class allowed_sender_item(SettingValueBase):
    tag = 'allowed_sender_item'
    name = 'Кто может кидать вам предметы'
    emodzi = '📩'
    default_value = 'all'
    default_value_type = Literal['all', 'friends', 'none']
    redact_values = ['all', 'friends', 'none', DEFAULT]

class SettingSelf:
    all_parameters: list[type[SettingValueBase]] = [
        #is_receive_news,
        is_receive_friedship_requests,
        is_hide_in_top,
        #is_hide_char,
        allowed_sender_item,
    ]
    
    DEFAULT = DEFAULT
    parameters_tags = {a.tag:a for a in all_parameters}
    faqs = [a.faq() for a in all_parameters if a.faq()]

