from app.interlayer.base import BaseLayer
from app.logic.setting import SettingLogic

class SettingLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = SettingLogic()

    async def get_setting(self, type: str):
        await self.get_char_info()
        await self.logic.check_setting(type, self.user, self.char)
        await self.get_char_info()
        match type:
            case 'user':
                return self.user.parametrs
            case 'char':
                return self.char.parametrs

    async def redact_setting(self, tag: str, type: str):
        await self.get_char_info()
        return await self.logic.redact_setting(tag, type, self.user, self.char)

    async def insert_json(self, data: dict, type: str):
        await self.get_char_info()
        return await self.logic.insert_json(data, type, self.user, self.char)
