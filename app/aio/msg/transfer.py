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

    def to_status_text(self, status: str):
        match status:
            case 'confirmed':
                return '🎗️ Произойдет обмен предметами между персонажами:'
            case 'created':
                return '✒️ Черновик сделки обмена предметами между персонажами:'
            case 'rejected':
                return '❌ Отклонена сделка обмена предметами между персонажами:'
            case 'completed':
                return '✅ Успешная сделка обмена предметами между персонажами:'
            case _:
                return '🎗️ Сделка обмена предметами между персонажами:'

    def temperate(self, char_emodzi: str, char: CharacterDB, items: list[ItemDB] | None = None):
        return f'{char_emodzi} {char.exist.full_name} {' (Вы)' if self.seller_id == char.id else ''}' + TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт.)' for item in items]) if items else '❌').blockquote()

    def text(self, emodzi1: str = '👤', emodzi2: str = '👤', status: str = 'confirmed'):
        return self.to_status_text(status) + '\n \n' +  self.temperate(emodzi1, self.char1, self.items1) + '\n \n' + self.temperate(emodzi2, self.char2, self.items2)
    
class InfoTransferText:
    def search_text(search_type: str):
        if search_type == 'transfer_id':
            return '✒️ Отправьте ID сделки'
        elif search_type == 'char_id':
            return '✒️ Отправьте ID персонажа, с которым вы заключали сделку'
        elif search_type == 'item_id':
            return '✒️ Отправьте ID предмета в сделке'

    def to_transfer_id(transfer_id: str | int):
        return TextHTML(f'/transfer {transfer_id}').code()

