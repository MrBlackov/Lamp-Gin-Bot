from app.db.metods.gets import get_all_chars, get_item_sketchs, get_items, get_all_transfers, get_users
from app.db.metods.unique import get_all_objs, Base
from app.logic.cls import Stats
from datetime import datetime, date, time, timedelta
from app.logic.utils import generate_date_range
from zoneinfo import ZoneInfo

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
                                        sep: timedelta =timedelta(days=1)) -> dict[date, list[Base]]:
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
