from app.aio.msg.utils import TextHTML
from app.logic.cls import Stats

class StatsText:
    def __init__(self, stats: Stats):
        self.stats = stats

    @property
    def all_coins(self):
        return '📋 Стаистика по количеству' + TextHTML('\n'.join([
            f'Пользователей - {self.stats.coins.users_coins}',
            f'Персонажи - {self.stats.coins.chars_coins}',
            f'Предметов - {self.stats.coins.items_coins}',
            f'Эскизов предметов - {self.stats.coins.item_sketchs_coins}',
            f'Сделок - {self.stats.coins.transfers_coins}',
        ])).blockquote()


