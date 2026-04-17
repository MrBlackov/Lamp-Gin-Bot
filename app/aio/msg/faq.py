from app.aio.msg.utils import TextHTML
from app.exeption import BotError

class FaqText:
    def __init__(self, error: BotError):
        self.error = error

    def help_error_faq(self):
        error_faq_dict = {
            f'🆔 Код ошибки: ': self.error.code,
            f'💬 Сообщение: ': self.error.msg,
            f'📖 Справка: ': self.error.faq 
        }
        return '📚 Информация по ошибке' + TextHTML('\n'.join([TextHTML(e).bold + v for e, v in error_faq_dict.items()])).blockquote()
    
    def to_start(name: str):
        return (
            f'👋 Приветствую вас, {TextHTML(name).bold}! Что сделаем для начала? \n\n'
            'Создать персонажа - /newchar \n'
            'Получить справку - /help \n'
            'Посмотреть список команд - /helpcmd'
            )

    def help_cmd(is_admin: bool = False):
        text_dict = {
            '/mychar ':' - Посмотреть список ваших персонажей и выбрать действующего',
            '/inventory ':' - Открыть инвентарь действующего персонажа',
            '/transfer ':' - Посмотреть свои сделки',
            '/transfer {id} ':' - Посмотреть информацию о сделке с помощью id (указывать вместо {id})',
            '/craft':' - Посмотреть доступные крафты',
            '/newchar ':' - Создать нового персонажа',
            '/newtransfer ':' - Заключить новую сделку',
            '/newitem':' - Создать новый предмет',
            '/newcraft':' - Создать новый крафт',
            '\n/chat':' - Открыть настройки чата',
            '/items ':' - Посмотреть список всех предметов в боте',
            '/help ':' - Получить общую справку',
            '/helpcmd ':' - Получить справку об командах',
            '/helpitem':' - Получить справку о предмете',
            '/helperror {code} ':' - Получить справку про возникшую ошибку, код которой указывайте в одном сообщении с командой (вместо {code})'
        }
        admin_text_dict = {
            '/additem name:{name}, emodzi:{emodzi}, size:[size] ':' - Cоздать предмет с заданными характеристиками.',
            '/changeitem id:{id} ':' - Изменить предмет',
            '/giveitem id:{id}, quantity:{quantity} ':' - Выдать себе предмет',
            '\n {} ':' - обязательные аргументы',
            ' [] ':' - не обязательные аргументы',
        }
        text = '\n'.join(TextHTML(k).bold + v for k, v in text_dict.items())
        admin_text = '\n \n 📟 Команды для админа \n \n' + '\n'.join(TextHTML(k).bold + v for k, v in admin_text_dict.items())
        return  '📜 Список доступных команд \n\n' + text + (admin_text if is_admin else '')
  
    def help_char_faq():
        return 'Скоро'
    
    def help():
        return (
            '📚 Краткая справка по боту \n\n'
            f'Бот создан по мотивам {TextHTML('Lord of the Mysteries').bold}. '
            'Здесь вы можете создавать персонажей, управлять инвентарем, заключать сделки и создавать свои предметы. \n\n'
            '📜 Команды ' +
            TextHTML(
            ' /mychar - Посмотреть список ваших персонажей и выбрать действующего \n'
            ' /inventory - Открыть инвентарь действующего персонажа \n'  
            ' /transfer - Посмотреть свои сделки \n'
            ' /craft - Посмотреть доступные крафты \n'
            ' /help - Получить общую справку \n'
            ' /helpcmd - Получить справку по командам'
            ).blockquote() + '\n'
            'Если у вас возникнут вопросы или проблемы, не стесняйтесь обращаться за помощью к @mr_blackov.'
        )

    def item_rules():
        return (
            '📜 Требования к эскизам предметов \n\n'
            '1. Эскиз не должен нарушать правила Telegram. \n'
            '2. Эскиз должен быть уникальным и реалистичным. \n'
            '3. Соблюдение требований повышает шансы на одобрение эскиза, но не гарантирует его создания. \n'
        )

    def help_items():
        return '📚 Справка по предметам' + TextHTML('\n'.join([TextHTML(k).bold + v for k, v in {
            '⏲️ Вес одного':' - сколько весит один предмет',
            '🎲 Шанс выпадения':' - шанс присуствия этого предмета в инвентаре создаваемого персонажа',
            '📈 Макс. выпадения':' - минимальное количество предмета в инвентаре создаваемого персонажа',
            '📉 Мин. выпадения':' - максимальное количество предмета в инвентаре создаваемого персонажа',
            }.items()])).blockquote()
    
    def help_chars():
        return 'Скоро'
