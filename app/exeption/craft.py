from app.exeption.base import BotError

class CraftError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Крафтов'
    code = '500.4'
    faq = 'Эта ошибка в системе Крафтов возникает, если разработчик не предусмотрел все ситуации. Пожалуйста, сообщите ему об ошибки и когда она возникла.'

class CraftQuantityNoIntError(CraftError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.9'
    faq = ''

class CraftQuantityLessOneError(CraftError):
    msg = '❌ Вы отправили число меньше 1, отправьте число равное 1 или больше 1.'
    code = '402.10'
    faq = ''

class CraftNoHaveIngredientsError(CraftError):
    msg = '❌ Вы не добавили ни одного ингредиента'
    code = '402.11'
    faq = '💮 Нажмите на \'+\' если хотите добавить предмет в ингредиенты'

class CraftNoHaveResultsError(CraftError):
    msg = '❌ Вы не добавили ни одного результата крафта'
    code = '402.12'
    faq = '⚗️ Нажмите на \'+\' если хотите добавить предмет в результат'
    
class CraftNoHaventItemError(CraftError):
    msg = '❌ У вас нет предмета для крафта или его недостаточно'
    code = '402.13'
    faq = ''

class CraftNoHaventToolError(CraftError):
    msg = '❌ У вас нет инструмента для крафта или его недостаточно'
    code = '402.13'
    faq = ''


    