from app.exeption.base import BotError
from app.logged.botlog import logs

class ValidToTypeError(BotError):
    msg = '❌ У значения неправильный тип (401.1)'

class ValidToIntError(ValidToTypeError):
    msg = '❌ Введите число (401.2)'

class ValidToIntPositiveError(ValidToTypeError):
    msg = '❌ Введите число больше 0 (401.3)'

class ValidToStrLenError(ValidToTypeError):
    def __init__(self, *args, len: int, max_len: int, level: str ='warning', **kwargs):
        super().__init__(*args, level=level, len=len, max_len=len, **kwargs)
        self.msg = f'❌ Введите значение меньше {max_len} символов, у вас {len} (401.4)'

class ValidToStrError(ValidToTypeError):
    msg = '❌ Отправьте только текст (401.5)'
