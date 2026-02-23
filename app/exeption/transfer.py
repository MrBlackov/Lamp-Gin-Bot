from app.exeption.base import BotError
from app.logged.botlog import logs

class TransferError(BotError):
    msg = '⁉️ Неизвестная ошибка в сделках'
    code = '500.5'
    faq = ''

class TransferQuantityNoIntError(TransferError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.8'
    faq = ''

class TransferNoHaventItemError(TransferError):
    msg = '❌ У вас нет предмета для сделки или его недостаточно'
    code = '402.9'
    faq = ''
    
class TransferSellerNoHaventItemError(TransferError):
    msg = '❌ У вашего партнера нет предмета для сделки или его недостаточно'
    code = '402.9'
    faq = ''
    
class TransferNoFindError(TransferError):
    msg = '❌ Сделка не найдена'
    code = '402.10'
    faq = ''

class TransferEnoughError(TransferError):
    msg = '❌ Сделка должна передавать предмет хотя бы в одну сторону '
    code = '402.11'
    faq = 'В вашей сделке не указаны предметы для обмена. Укажите хотя бы один предмет'