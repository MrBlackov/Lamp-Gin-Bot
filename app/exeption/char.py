from app.exeption.base import BotError

class CharError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Персонажей'
    code = '500.3'

class CharHastNameError(CharError):
    msg = '⁉️ Персонаж Безымянный, буквально...'    
    code = '500.1'


class InventaryOverFlowing(CharError):
    msg = '❌ Инвентарь будет переполнен, предмет невозможно получить'
    code = '402.7'
