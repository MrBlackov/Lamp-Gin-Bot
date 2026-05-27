from app.exeption.base import BotError

class DropError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Сундуков'
    code = '522.1'
    faq = ''

class DropNotFoundError(DropError):
    msg = '❌ Сундуков в округе не найдено'
    code = '522.2'
    faq = 'Сундуки в округе появляются в случайное время, попробуйте позже'

class ChatDontReceiveDropError(DropError):
    msg = '❌ В этом чате выключено получение дропов'
    code = '522.2'
    faq = 'Чтобы включить получение дропов в чате, владелец чата должен включить эту функцию в настройках чата'

class PrivateChatDontReceiveDropError(DropError):
    msg = '❌ Дропы недоступны в личных чатах'
    code = '522.3'
    faq = 'Сундуки в личных чатах недоступны, так как они предназначены для групповых чатов. Чтобы получать дропы, пригласите бота в групповой чат и включите получение дропов в настройках чата'

class DropEmptyError(DropError):
    msg = '❌ Сундук пустой'
    code = '522.4'
    faq = ''
