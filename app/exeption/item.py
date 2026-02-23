from app.exeption.base import BotError

class ItemError(BotError):
    msg = '⁉️ Неизвестная ошибка в системе Предметов'
    code = '500.2'
    faq = 'Эта ошибка в системе Предметов возникает, если разработчик не предусмотрел все ситуации. Пожалуйста, сообщите ему об ошибки и когда она возникла.'

class NotNameItemSketchError(ItemError):
    msg = '❌ В вашем эскизе отсуствует имя'
    code = '401.6'
    faq = 'Вы забыли указать имя в эскизе предмета'

class NameNoValideError(ItemError):
    msg = '❌ В вашем имени эскиза больше 30 символов'
    code = '401.7'
    faq = 'Вы указали имя эскиза, но его длина превышает 30 символов. Укажите имя, длина которого меньше 30 символов. Пробелы тоже считаются.'

class EmodziNoValideError(ItemError):
    msg = '❌ Эмозди должен быть один'
    code = '401.8'
    faq = 'Вы указали эмодзи, длина котрого больше 1 символа, отправьте 1 эмодзи.'
    
class SizeNotIntItemSketchError(ItemError):
    msg = '❌ Вес должен быть челым числом'
    code = '401.1й'
    faq = 'Вы отправили вес десятичным числом, нужно целое число.'

class SizeLessOneItemSketchError(ItemError):
    msg = '❌ Вес должен быть целым числом больше нуля'
    code = '401.12'
    faq = 'Вы отправили число меньше нуля, нужно целое число больше нуля. Вес не может быть меньше или равен нулю'

class DropNotIntItemSketchError(ItemError):
    msg = '❌ Это значение должно быть целым числом'
    code = '401.13'
    faq = 'Вы отправили не целое число, нужно целое число.'

class DropLessZeroItemSketchError(ItemError):
    msg = '❌ Это значение должно быть целым числом больше нуля'
    code = '401.14'
    faq = 'Вы отправили число меньше нуля, нужно целое число больше нуля.'

class NameNoValideError(ItemError):
    msg = '❌ Значение должно быть bool-типа(0 или 1)'
    code = '401.15'
    faq = 'Вы отправили значение не того типа, отправьте 0 или 1'

class RariryValideError(ItemError):
    msg = '❌ Значение должно быть числом от 0 до 1 с плавающей точкой'
    code = '401.16'
    faq = 'Вы отправили значение не того типа, отправьте число от 0 до 1 с плавающей точкой. Например, 0.1 будет означать 10% шанс выпадения'

class MaxDropLessMinDropError(ItemError):
    msg = '❌ Значение максимального дропа должно быть больше чем значение минимального дропа'
    code = '401.17'
    faq = ''
 




class NoFindItemSketchForID(ItemError):
    msg = '❌ Эскиз предмета с таким ID не найден, попробуйте поискать в /items'
    code = '401.10'
    faq = 'Вы отправили ID эскиза, которого не сущействует, посмотрите ID эскиза нужного вам предмета в /items и отправьте его'



class ItemNoHideCreatedError(ItemError):
    msg = '⁉️ Этот предмет уже был создан и промодерирован'
    code = '501.3'
    faq = 'Если вам пришла эта ошибка, сообщите об этом разработчику'
    




class ThrowAwayQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля'
    code = '402.1'
    faq = ''
    
class ThrowAwayQuantityMoreItemQuantity(ItemError):
    msg = '❌ Вы отправили число, которое больше того, что у вас есть'
    code = '402.2'
    faq = ''

class ThrowAwayQuantityNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.3'
    faq = ''

class ThrowAwayQuantityFloat(ItemError):
    msg = '❌ Вы отправили не целое число. Нужно целое число'
    code = '402.14'  
    faq = ''  


class GiveItemQuantityLessOne(ItemError):
    msg = '❌ Вы отправили число меньше или равное нулю. Нужно целое число, которое больше нуля'
    code = '402.4'
    faq = ''

class GiveItemNoEnterNameOrID(ItemError):
    msg = '❌ Вы не указали ни имя, ни айди нужного предмета'
    code = '402.5'
    faq = ''

class GiveItemNoEnterID(ItemError):
    msg = '❌ Вы не указали айди нужного предмета'
    code = '402.5' 
    faq = ''   
   
class GiveItemNoInt(ItemError):
    msg = '❌ Вы отправили не число. Нужно число'
    code = '402.6'
    faq = ''
 

