from app.exeption.base import BotError

class ActionError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Персонажей'
    code = '510.1'

class StopError(BotError):
    msg = '❌ Ваш персонаж чем-то занят'
    code = '510.2'
    faq = 'Ваш персонаж чем-то занят и не может выполнять действия. Подождите, пока он закончит, или остановите его с помощью команды - /stop.'

class SleepError(StopError):
    msg = '💤 Ваш персонаж спит'
    code = '510.3'
    faq = 'Ваш персонаж спит и не может выполнять действия. Подождите, пока он проснется, или разбудите его с помощью команды - /wake_up.'

class SleepCoinsError(BotError):
    msg = '💤 Ваш персонаж полон сил'
    code = '510.8'
    faq = 'Ваш персонаж не может заснуть. Потратьте сначала энергию (персонаж может заснуть когда у него меньше 100 энергии).'

class ActionQuantityLessOne(ActionError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля'
    code = '510.4'
    faq = ''
 

class ActionQuantityNoInt(ActionError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '510.6'
    faq = ''

class ActionQuantityFloat(ActionError):
    msg = '❌ Вы отправили не целое число. Нужно целое число'
    code = '510.7'  
    faq = ''  

class NotNewStatsError(ActionError):
    msg = '❌ Обновлений нету'
    code = '510.9'
    faq = ''   
    
class HaveItemError(ActionError):
    msg = '❌ У вас нету нужных предметов'
    code = '510.10'
    faq = ''  

class HaveSkillError(ActionError):
    msg = '❌ У вас нету нужных навыков'
    code = '510.11'
    faq = ''  

class EnergyLessZeroError(ActionError):
    msg = '❌ Ваш персонаж устал'
    code = '510.11'
    faq = 'Ваша энергия упала ниже 0, отдохните'    

class DiceCmdNoValideError(ActionError):
    msg = '❌ В команде присуствуют лишние знаки'
    code = '510.12'
    faq = 'Ваша команда не валидна, синтаксис: kdn + m'    

class DiceCmdDontHaveDError(ActionError):
    msg = '❌ В команде отсуствует "d"'
    code = '510.13'
    faq = 'Ваша команда не валидна, символа "d" нет в команде'    

class DiceCmdLongError(ActionError):
    msg = '❌ Результат команды слишком большой, сделайте выборку меньше'
    code = '510.14'
    faq = 'Сообщение слишком большое'    

class PaperLongError(ActionError):
    msg = '❌ Надпись сликом большая, сделайте поменьше'
    code = '510.15'
    faq = 'Длина вашеей надписи должна быть меньше 2000' 

class BookDontHaveInfoError(ActionError):
    msg = '❌ Сначало назовите книгу через ее настройки'
    code = '510.16'
    faq = '' 

class BookSettingCloseError(ActionError):
    msg = '❌ Эту книгу нельзя редактировать'
    code = '510.16'
    faq = '' 