from app.exeption.base import BotError


class MainError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе'
    code = '500.4'
    faq = 'Эта ошибка в системе возникает, если разработчик не предусмотрел все ситуации. Пожалуйста, сообщите ему об ошибки и когда она возникла.'

class MainQuantityLessSixTeen(MainError):
    msg = '❌ Вы отправили число меньше 120. Нужно целое число, которое больше 120'
    code = '402.17'
    faq = ''

class MainQuantityMaxTime(MainError):
    msg = '❌ Вы отправили число больше 170.000. Нужно целое число, которое меньше 170.000'
    code = '402.17'
    faq = 'Виду особенностей работы Telegram, время удаления сообщения не может быть больше 170.000 секунд (около 47 часов). Пожалуйста, укажите число меньше 170.000.'

class MainQuantityNoInt(MainError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.18'
    faq = ''

class MainQuantityFloat(MainError):
    msg = '❌ Вы отправили не целое число. Нужно целое число'
    code = '402.19'  
    faq = ''  

class NoDeleteMessageError(MainError):
    pass
