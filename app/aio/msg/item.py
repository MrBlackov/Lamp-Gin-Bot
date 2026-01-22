from app.validate.sketchs.item_sketchs import ItemSketch
from app.aio.msg.utils import TextHTML

class AddItemText:
    def __init__(self, sketch: ItemSketch):
        self.sketch = sketch
 
    @property
    def temperate(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '{EMOJI_TYPE} Тип: {TYPE}',
            '📊 Кол-во: {QUANTITY}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote(True)
 
    @property    
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            TYPE=self.sketch.type.to_rus(),
            EMOJI_TYPE=self.sketch.type.to_emodzi(),
            QUANTITY=self.sketch.quantity,
            DESCRIPT=self.sketch.descriprtion if self.sketch.descriprtion else '❌'
        )
        return value
