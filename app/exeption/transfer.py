from app.exeption.base import BotError
from app.logged.botlog import logs

class TransferError(BotError):
    msg = '⁉️ Неизвестная ошибка в сделках'
    code = '500.5'

class TransferQuantityNoInt(TransferError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.8'