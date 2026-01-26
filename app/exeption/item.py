from app.exeption.base import BotError

class ItemError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Предметов (500.2)'

class NotNameItemSketchError(ItemError):
    msg = '❌ В вашем эскизе отсуствует имя (401.6)'

class NameNoValideError(ItemError):
    msg = '❌ В вашем имени эскиза больше 30 символов (401.7)'

class EmodziNoValideError(ItemError):
    msg = '❌ Эмозди должен быть один (401.8)'
    