from app.exeption.base import BotError
from app.logged.botlog import logs

class SettingError(BotError):
    msg = '⁉️ Непредвиденная ошибка'
    code = '420.1'
    faq = ''

class SettingTagError(SettingError):
    msg = '❌ Нет такого параметра'
    code = '420.2'
    faq = ''
    
class SettingValueError(SettingError):
    msg = '❌ Значение параметра не валидно'
    code = '420.3'
    faq = ''
