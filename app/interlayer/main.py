from app.db.metods.gets import get_user_for_tg_id, get_main_char_for_user_id, get_char_for_id, get_item_for_name, get_user_for_id


class UserLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def get_char_info(self, user_id: int | None = None):
        if user_id:
            self.user = await get_user_for_id(user_id)
        else:
            self.user = await get_user_for_tg_id(self.tg_id, True)
        self.char_id = await get_main_char_for_user_id(self.user.id)
        self.char = await get_char_for_id(self.char_id)
        return self





