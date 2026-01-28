from app.exeption.base import BotError

class AnotherError(BotError):
    msg = '⁉️ Неизвестная ошибка в Боте'
    code = '500.4'

class DiceError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Костей'
    code = '501.2'


