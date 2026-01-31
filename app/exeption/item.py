from app.exeption.base import BotError

class ItemError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Предметов'
    code = '500.2'

class NotNameItemSketchError(ItemError):
    msg = '❌ В вашем эскизе отсуствует имя'
    code = '401.6'

class NameNoValideError(ItemError):
    msg = '❌ В вашем имени эскиза больше 30 символов'
    code = '401.7'

class EmodziNoValideError(ItemError):
    msg = '❌ Эмозди должен быть один'
    code = '401.8'
    
class ThrowAwayQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля'
    code = '402.1'
    
class ThrowAwayQuantityMoreItemQuantity(ItemError):
    msg = '❌ Вы отправили число, которое больше того, что у вас есть'
    code = '402.2'

class ThrowAwayQuantityNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.3'
    
class GiveItemQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля'
    code = '402.4'

class GiveItemNoEnterNameOrID(ItemError):
    msg = '❌ Вы не указали ни имя, ни айди нужного предмета'
    code = '402.5'

class GiveItemNoEnterID(ItemError):
    msg = '❌ Вы не указали айди нужного предмета'
    code = '402.5'    
   
class GiveItemNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.6'
 

