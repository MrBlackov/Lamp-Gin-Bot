from app.aio.msg.utils import TextHTML
from app.db.models.item import CraftDB
from app.validate.craft import CraftValide

class CraftText:
    def __init__(self, craft: CraftDB | CraftValide):
        self.craft = craft

    def text(self, quantity: int = 1, is_create: bool = False) -> str:
        return (
            '📜 Рецепт \n\n' 
            f'⏱️ Время крафта: {self.craft.time} секунд\n'
            #f'{f'📰 Скрытый: {'✅' if self.craft.is_hide else '❌'}\n' if is_create else ''}'
            f'\n💮 Ингредиенты: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity*quantity}шт. {f"x{quantity}" if quantity > 10000 else ""})' for item in self.craft.ingredients] if len(self.craft.ingredients) > 0 else "❌")).blockquote()}' 
            f'\n🛠️ Инструменты: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity}шт.)' for item in self.craft.tools] if len(self.craft.tools) > 0 else "❌")).blockquote()}' 
            f'\n⚗️ Результат: {TextHTML('\n'.join([f'{item.sketch.emodzi} {item.sketch.name} ({item.quantity*quantity}шт. {f"x{quantity}" if quantity > 100000 else ""})' for item in self.craft.results] if len(self.craft.results) > 0 else "❌")).blockquote()}' 
            )

    def faq(faq_type: str):
        match faq_type:
            case 'ingredients':
                return "💮 Нажмите на '+' если хотите добавить предмет в ингредиенты, и на '-' если хотите убрать"
            case 'tools':
                return "🛠️ Нажмите на '+' если хотите добавить предмет в инструменты, и на '-' если хотите убрать"
            case 'results':
                return "⚗️ Нажмите на '+' если хотите добавить предмет в результат, и на '-' если хотите убрать"
        return "📜 Нажмите на '+' если хотите добавить предмет, и на '-' если хотите убрать"

