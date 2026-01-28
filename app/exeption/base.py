from app.logged.botlog import logs
from typing import Literal    

class BotError(Exception):
    msg = '🐞 Непредвиденная ошибка в боте'
    code = '500.1'
    faq = ''

    def __init__(self, *args, level: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'warning', **kwargs):
        self.level = level
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args)
        getattr(logs, level)(f'{self.__class__.__name__}, msg: {self.args}, kwargs: {self.kwargs}')

    def __str__(self):
        return super().__str__()
    
    @property
    def to_msg(self):
        return self.msg + f' ({self.code})'

def msg_error(bot_error: BotError | list[BotError]) -> str | list[str]:
    if type(bot_error) == BotError: return bot_error.to_msg()
    elif type(bot_error) == list:
        return [e.to_msg() for e in bot_error]
    else:
        raise AttributeError(f'Error to msg_error, bot error: {bot_error}')
    
error_faq: dict[str, BotError] = {}

def get_sub_exeptions(cls):

    """Рекурсивно получаем все дочерние классы"""
    all_subclasses = []
    
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_sub_exeptions(subclass))
    
    return all_subclasses

def get_error_faq():
    sub_exeptions: list[BotError] = get_sub_exeptions(BotError)
    for error in sub_exeptions:
        error_faq |= {error.code: error}