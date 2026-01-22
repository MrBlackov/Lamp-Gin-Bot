from app.logged.botlog import logs
from typing import Literal

class BotError(Exception):
    msg = '🐞 Непредвиденная ошибка в боте (500.1)'

    def __init__(self, *args, level: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'warning', **kwargs):
        self.level = level
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args)
        getattr(logs, level)(f'{self.__class__.__name__}, msg: {self.args}, kwargs: {self.kwargs}')

    def __str__(self):
        return super().__str__()
    
    @classmethod
    def __to_msg__(cls) -> str:
        return cls.msg

def msg_error(bot_error: BotError | list[BotError]) -> str | list[str]:
    if type(bot_error) == BotError: return bot_error.__to_msg__()
    elif type(bot_error) == list:
        return [e.__to_msg__() for e in bot_error]
    else:
        raise AttributeError(f'Error to msg_error, bot error: {bot_error}')
    
