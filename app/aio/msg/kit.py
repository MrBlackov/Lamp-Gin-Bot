from app.db.models.item import KitDB, KitSketchDB, ItemSketchDB
from app.db.models.char import CharacterDB
from app.aio.msg.utils import TextHTML

class KitText:
    def __init__(self, kit: KitDB | None = None, sketch: KitSketchDB | None = None):
        self.kit = kit
        self.sketch = kit.sketch if kit else sketch 

    def text(self, items: list[ItemSketchDB], is_new: bool = False):
        one_items = [item.emodzi + ' ' + item.name for item in items if item.rarity == 1]
        another_items = [item.emodzi + ' ' + item.name for item in items if 0 < item.rarity < 1]
        return (('🆕' if is_new else '🟢') + ' ' + self.sketch.name + 
                ' \n\n Предметы выпадающие с 100% шансом' + 
                TextHTML('\n'.join(one_items)).blockquote() + 
                ' \n Предметы выпадающие с неким шансом' + 
                TextHTML('\n'.join(another_items)).blockquote(True))
    