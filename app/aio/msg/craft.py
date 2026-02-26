from app.aio.msg.utils import TextHTML
from app.db.models.item import CraftDB

class CraftText(TextHTML):
    def __init__(self, craft: CraftDB):
        self.craft = craft

    @property
    def text(self) -> str:
        return (
            '📜 Рецепт крафта \n' 
            f'\n Ингредиенты: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт.)' for item in self.craft.ingredients])).blockquote()}' 
            f'\n Результат: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт.)' for item in self.craft.results])).blockquote()}' 
            f'\n Инструменты: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт.)' for item in self.craft.tools])).blockquote()}' 
            )



