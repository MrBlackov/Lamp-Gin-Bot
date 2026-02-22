from app.exeption.base import BotError
from app.logged.botlog import logs

class ValidToTypeError(BotError):
    msg = '❌ У значения неправильный тип'
    code = '401.1'
    faq = ''

class ValidToIntError(ValidToTypeError):
    msg = '❌ Введите число'
    code = '401.2'
    faq = ''

class ValidToIntPositiveError(ValidToTypeError):
    msg = '❌ Введите число больше 0'
    code = '401.3'
    faq = ''

class ValidToStrLenError(ValidToTypeError):
    def __init__(self, *args, len: int, max_len: int, level: str ='warning', **kwargs):
        super().__init__(*args, level=level, len=len, max_len=len, **kwargs)
        self.msg = f'❌ Введите значение меньше {max_len} символов, у вас {len}'
    code = '401.4'
    faq = ''

class ValidToStrError(ValidToTypeError):
    msg = '❌ Отправьте только текст'
    code = '401.5'
    faq = ''

class ValidStrToJSONError(ValidToTypeError):
    msg = "❌ Значение должно содержать знак ':'"
    code = '401.9'
    faq = ''

