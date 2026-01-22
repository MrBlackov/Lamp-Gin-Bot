from app.exeption.base import BotError

class AnotherError(BotError):
    msg = '⁉️ Неизвестная ошибка в Боте (500.4)'

class DiceError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Костей (501.2)'


