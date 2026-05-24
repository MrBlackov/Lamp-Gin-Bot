from app.exeption.base import BotError

class CharError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Персонажей'
    code = '500.3'

class SKillLessOneError(CharError):
    msg = '❌ Этот навык нельзя нельзя сделать пониже'    
    code = '502.2'

class SKillLessZeroError(CharError):
    msg = '❌ Вы уже убрали навык'    
    code = '502.3'

class SKillCoinsLessZeroError(CharError):
    msg = '❌ У вас недостаточно 💮 Очков навыка'
    code = '502.4'

class CharHastNameError(CharError):
    msg = '⁉️ Персонаж Безымянный, буквально...'    
    code = '500.7'

class BonusCharSubError(CharError):
    msg = '❌ Вы не подписались на канал'    
    code = '405.1'

class NoHaveMainChar(CharError):
    msg = '❌ У вас не выбран действующий персонаж'    
    code = '503.1'  
    faq = 'Чтобы выбрать используйте команду /mychars и выберите из списка нужного персонажа'  

class InventaryOverFlowing(CharError):
    msg = '❌ Инвентарь будет переполнен, предмет невозможно получить'
    code = '402.7'

class InventaryNoHaveError(CharError):
    msg = '❌ Такова количества этого предмета нет у вас'
    code = '402.8'

class NoDeleteCharError(CharError):
    msg = '❌ У вас кончилась веревка'
    code = '505.1'
    faq = 'Удалить персонажа можно только один раз (пока что)'

