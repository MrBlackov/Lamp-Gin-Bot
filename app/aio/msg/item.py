from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB
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

class ItemSketchText:
    def __init__(self, sketch: ItemSketchDB):
        self.sketch = sketch
 
    @property
    def temperate(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '♣️ Эскиз ID: {ID}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
 
    @property
    def temperate_admin(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '👤 Создатель: {USER_ID}',
            '♣️ Эскиз ID: {ID}',
            '⏲️ Вес одного: {WEIGHT}кг',
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
            ID=self.sketch.id
        )
            return value
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ID=self.sketch.id
        )
        return value

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