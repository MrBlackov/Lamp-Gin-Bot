from app.exeption.base import BotError
from app.aio.msg.utils import TextHTML

class FaqError(BotError):
    msg = '⁉️ Неизвестная ошибка в FAQ'
    code = '500.6'
    faq = ''

class FaqErrorNoEnterError(BotError):
    msg = '❌ Отправьте вместе с командой код ошибки'
    code = '402.12'
    faq = f'Вы отправили команду без указания кода ошибки. Пример - {TextHTML('/help error 500.1').code}'

class FaqErrorNoFindError(BotError):
    msg = '❌ Ошибка с таким кодом не существует'
    code = '402.13'
    faq = ''



