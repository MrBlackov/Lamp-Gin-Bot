from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.aio.msg.utils import TextHTML

class ItemText:
    def __init__(self, item: ItemDB):
        self.sketch = item.sketch
        self.item = item
 
    @property
    def temperate(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '♠️ Предмет ID: {ITEMID}',
            '♣️ Эскиз ID: {SKETCHID}',
            '📊 Кол-во: {QUANTITY}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🧳 Общий вес: {ALLWEIGHT}кг',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()    
 
    @property    
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            QUANTITY=self.item.quantity,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ALLWEIGHT=self.sketch.size*self.item.quantity/1000,
            ITEMID=self.item.id,
            SKETCHID=self.sketch.id
        )
        return value

class NewItemText:
    def __init__(self, sketch: ItemSketchValide):
        self.sketch = sketch
 
    @property
    def temperate(self):
        if self.sketch.rarity == 0:
            return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
    
    def text(self):
        if self.sketch.rarity == 0:
            return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6]
        )
        return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6],
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop
        )

    def to_redact_text(redact_key: str):
        match redact_key:
            case 'name':
                return '✒️ Отправьте имя предмета. Количество символов должно быть не больше 30'
            case 'emodzi':
                return '✒️ Отправьте эмодзи для предмета. Эмодзи должен быть 1'
            case 'size':
                return '✒️ Отправьте вес одного предмета в граммах. Вес должен быть целым числом'
            case 'description':
                return '✒️ Отправьте описание для предмета. Количество символов должно быть не больше 200'
            case 'rarity':
                return '✒️ Отправьте редкость предмета в виде десятичной дроби от 0 до 1. Например, 0.1 будет означать 10% шанс выпадения'
            case 'max_drop':
                return '✒️ Отправьте максимальное количество предметов, которое может выпасть. Должно быть целым числом'
            case 'min_drop':
                return '✒️ Отправьте минимальное количество предметов, которое может выпасть. Должно быть целым числом и не больше максимального количества'
            case 'creator_id':
                return '✒️ Отправьте user_id создателя'
            case _:
                return '✒️ Отправьте значение'

class ItemSketchText:
    def __init__(self, sketch: ItemSketchDB):
        self.sketch = sketch
 
    @property
    def temperate(self):
        if self.sketch.rarity == 0:
            return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
 
    @property
    def temperate_admin(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '👤 Создатель: {USER_ID}',
            '♣️ Эскиз ID: {ID}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
    
    def text(self, is_admin: bool = False):
        if is_admin:
            value = self.temperate_admin.format(
            USER_ID=self.sketch.creator_id,
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ID=self.sketch.id,
            RARITY=self.sketch.rarity*100,
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop
        )
            return value
        if self.sketch.rarity == 0:
            return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6]
        )
        return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6],
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop
        )

class CharItemText:    
    def __init__(self, char: CharacterDB, item: ItemDB):
        self.sketch = item.sketch
        self.item = item
        self.char = char

    @property
    def temperate(self):
        return ''.join(['{FULL_NAME}'+ TextHTML('\n'.join([
            '👤 ID: {CHARID}',
            '🪪 User ID: {USERID}',
            '💼 Макс. вес: {MAX_SIZE}кг'
        ])).blockquote(),
            '\n {EMODZI} {NAME}' + TextHTML('\n'.join([
            '♠️ Предмет ID: {ITEMID}',
            '♣️ Эскиз ID: {SKETCHID}',
            '📊 Кол-во: {QUANTITY}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🧳 Общий вес: {ALLWEIGHT}кг',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()])
    
    @property    
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            QUANTITY=self.item.quantity,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ALLWEIGHT=self.sketch.size*self.item.quantity/1000,
            ITEMID=self.item.id,
            SKETCHID=self.sketch.id,
            FULL_NAME=self.char.exist.full_name,
            CHARID=self.char.id,
            USERID=self.char.user_id,
            MAX_SIZE=self.char.exist.attibute_point.strength
        )
        return value