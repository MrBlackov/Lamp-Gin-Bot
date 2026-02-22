from app.exeption.base import BotError

class CharError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Персонажей'
    code = '500.3'

class CharHastNameError(CharError):
    msg = '⁉️ Персонаж Безымянный, буквально...'    
    code = '500.7'

class BonusCharSubError(CharError):
    msg = '❌ Вы не подписались на канал'    
    code = '405.1'

class NoHaveMainChar(CharError):
    msg = '❌ У вас не выбран действующий персонаж'    
    code = '503.1'    

class InventaryOverFlowing(CharError):
    msg = '❌ Инвентарь будет переполнен, предмет невозможно получить'
    code = '402.7'
