from app.exeption.base import BotError

class CharError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Персонажей (500.3)'

class CharHastNameError(CharError):
    msg = '⁉️ Персонаж Безымянный, буквально... (501.1)'

class InventaryOverFlowing(CharError):
    msg = '❌ Инвентарь будет переполнен, предмет невозможно получить (402.7)'