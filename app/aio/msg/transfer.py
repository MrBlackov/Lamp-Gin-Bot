from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB
from app.aio.msg.utils import TextHTML

class ItemTransferText:
    def __init__(self, char1: CharacterDB, char2: CharacterDB, items1: list[ItemDB] | None, items2: list[ItemDB] | None, seller_id: int | None = None):
        self.char1 = char1
        self.char2 = char2
        self.items1 = items1
        self.items2 = items2
        self.seller_id = seller_id if seller_id else char1.id

    def temperate(self, char_emodzi: str, char: CharacterDB, items: list[ItemDB] | None = None):
        return f'{char_emodzi} {char.exist.full_name} {' (Вы)' if self.seller_id == char.id else ''}' + TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт)' for item in items]) if items else '❌').blockquote()

    def text(self, emodzi1: str = '👤', emodzi2: str = '👤'):
        return 'Произойдет обмен предметами между персонажами: \n \n' +  self.temperate(emodzi1, self.char1, self.items1) + '\n \n' + self.temperate(emodzi2, self.char2, self.items2)