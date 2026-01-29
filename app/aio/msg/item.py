from app.db.models.item import ItemDB, ItemSketchDB
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
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            SKETCHID=self.sketch.id
        )
        return value
