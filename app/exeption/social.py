from app.exeption.base import BotError
from app.logged.botlog import logs

class SocialError(BotError):
    msg = '⁉️ Непредвиденная ошибка'
    code = '421.1'
    faq = ''

class NoFindUserError(SocialError):
    msg = '☹️ Этот пользователь еще не знает о Лампе'
    code = '421.2'
    faq = 'Пользователь не найден. Проверьте правильность его юзера.'

class EnterUserNameError(SocialError):
    msg = '😑 Вы отправили свой юзер. Отправьте юзер друга'
    code = '421.3'
    faq = ''

class UserFriendError(SocialError):
    msg = '😎 Вы уже друзья с этим пользователем. Отправьте юзер нового друга'
    code = '421.4'
    faq = ''
    
class NotReceiveFriendshipRequestError(SocialError):
    msg = '❌ Этот пользователь не принимает запросов дружбы'
    code = '421.5'
    faq = ''

