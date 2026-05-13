from app.db.metods.gets import get_all_chars, get_item_sketchs, get_items, get_all_transfers, get_users, get_all_skills, get_skills_for_tag
from app.db.metods.unique import get_all_objs, Base, get_char_settings_for_char_ids, get_chars_for_attribute_point_ids, get_skills_for_attribute_point_ids, CharacterDB, CharSettingDB
from app.logic.cls import Stats
from datetime import datetime, date, time, timedelta
from app.logic.utils import generate_date_range
from zoneinfo import ZoneInfo
from app.logic.settings import SettingSelf

class StatsLogic:
    async def get_all(self):
        users = await get_users()
        chars = await get_all_chars()
        item_sketchs = await get_item_sketchs()
        items = await get_items()
        transfers = await get_all_transfers()
        return Stats(users, chars, items, item_sketchs, transfers)

    async def get_datas_for_create_date(self, 
                                        table: Base, 
                                        start_date: date = date.today() - timedelta(30), 
                                        end_date: date = date.today(), 
                                        sep: timedelta = timedelta(days=1)) -> dict[date, list[Base]]:
        datas: list[Base] = await get_all_objs(table=table) 
        len(datas)
        date_range = [d.date() for d in generate_date_range(start_date, end_date)]
        results = {d:[] for d in date_range}
        for d in date_range:
            for data in datas:
                if d == data.created_at.date():
                    result: list = results.get(d, [])
                    result.append(data)
                    results[d] = result
                    
        return {d:r for d, r in results.items()}
    
    async def get_datas_for_create_time(self, 
                                        table: Base, 
                                        start_time: time = time(), 
                                        end_time: time = time(23), 
                                        sep: timedelta = timedelta(hours=1)) -> dict[date, list[Base]]:
        datas: list[Base] = await get_all_objs(table=table) 
        print(len(datas))
        date_range = [d.hour for d in generate_date_range(start_time=start_time, end_time=end_time, sep=sep)]
        print(date_range)
        results = {d:[] for d in date_range}
        print(results)
        for d in date_range:
            for data in datas:
                if d == data.created_at.astimezone(ZoneInfo('Europe/Moscow')).hour:
                    result: list = results.get(d, [])
                    result.append(data)
                    results[d] = result
                    
        return results
    
    def dict_coint(self, dictionary: dict, is_strict: bool = True):
        new_dict = {k:len(v) for k, v in dictionary.items() if hasattr(v, '__len__')}
        return new_dict if is_strict else dictionary | new_dict

    async def get_skills(self):
        return [s for s in await get_all_skills() if s.is_hide == False]
    
    async def topskill(self, skill_tag: str):
        skills = await get_skills_for_tag(skill_tag)
        skills = {s.attribute_point_id:s for s in skills}
        chars: list[CharacterDB] = await get_chars_for_attribute_point_ids(attribute_point_ids=skills.keys())
        char_settings: list[CharSettingDB] = await get_char_settings_for_char_ids(char_ids=[c.id for c in chars])
        char_settings = {c.char_id:c for c in char_settings}
        print(char_settings)
        chars = [(char.add_setting(char_settings.get(char.id), [a(char_settings.get(char.id)) for a in SettingSelf.all_parameters])) for char in chars]
        [char.exist.attibute_point.add_skills([skills.get(char.exist.attibute_point.id)]) for char in chars]
        return sorted(chars, key=lambda x: x.exist.attibute_point.skill_tags.get(skill_tag).level, reverse=True)
