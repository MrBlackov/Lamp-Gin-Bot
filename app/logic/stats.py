from app.db.metods.gets import get_all_chars, get_item_sketchs, get_items, get_all_transfers, get_users
from app.logic.cls import Stats


class StatsLogic:
    async def get_all(self):
        users = await get_users()
        chars = await get_all_chars()
        item_sketchs = await get_item_sketchs()
        items = await get_items()
        transfers = await get_all_transfers()
        return Stats(users, chars, items, item_sketchs, transfers)

