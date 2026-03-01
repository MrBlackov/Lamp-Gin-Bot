from app.exeption.base import BotError

class CraftError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Крафтов'
    code = '500.4'
    faq = 'Эта ошибка в системе Крафтов возникает, если разработчик не предусмотрел все ситуации. Пожалуйста, сообщите ему об ошибки и когда она возникла.'

class CraftQuantityNoIntError(CraftError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.9'
    faq = ''
