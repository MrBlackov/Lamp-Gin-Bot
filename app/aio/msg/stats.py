from app.aio.msg.utils import TextHTML
from app.logic.cls import Stats
from app.db.models.char import CharacterDB
from app.logic.settings import is_hide_in_top

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

    def topskill(skill_tag: str, results: list[CharacterDB]):
        skill = results[0].exist.attibute_point.skill_tags.get(skill_tag)
        return f'🏆 Топ персонажей ({skill.sketch.text})' + TextHTML.num_list([
            f'{result.exist.full_name if not(result.parametr_tags.get(is_hide_in_top.tag).value == True) else '???'} ({TextHTML.float_format(result.exist.attibute_point.skill_tags.get(skill_tag).level, 5)} ур.)' for result in results
            ]).blockquote()

 

  