from app.exeption.base import BotError

class ItemError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Предметов (500.2)'

class NotNameItemSketchError(ItemError):
    msg = '❌ В вашем эскизе отсуствует имя (401.6)'

class NameNoValideError(ItemError):
    msg = '❌ В вашем имени эскиза больше 30 символов (401.7)'

class EmodziNoValideError(ItemError):
    msg = '❌ Эмозди должен быть один (401.8)'
    
class ThrowAwayQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля (402.1)'
    
class ThrowAwayQuantityMoreItemQuantity(ItemError):
    msg = '❌ Вы отправили число, которое больше того, что у вас есть (402.2)'

class ThrowAwayQuantityNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число (402.3)'
    
class GiveItemQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля (402.4)'

class GiveItemNoEnterNameOrID(ItemError):
    msg = '❌ Вы не указали ни имя, ни айди нужного предмета (402.5)'
   
class GiveItemNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число (402.6)'
 

