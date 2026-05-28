from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.setting import SettingIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.setting import TextHTML, SettingText
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from app.interlayer.setting import SettingLayer
from app.aio.cls.fsm.utils import SettingFSM
import json
from app.aio.cls.fsm.setting import SettingState
from app.exeption.setting import SettingTagError, SettingValueError

class SettingService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = SettingLayer(tg_id)
        self.text = SettingText
        self.state = SettingFSM(state)
        self.IKB = SettingIKB(tg_id)

    @property
    def paramerts(self):
        return self.layer.logic.setting_self

    async def get_user_setting(self, type: str):
        settings = await self.layer.get_setting(type)
        return f'⚙️ Настройки {'аккаунта' if type == 'user' else 'персонажа'}', self.IKB.setting(settings, type)
     
    async def redact_setting(self, tag: str, type: str):
        settings = await self.layer.redact_setting(tag, type)
        return f'⚙️ Настройки {'аккаунта' if type == 'user' else 'персонажа'}', self.IKB.setting(settings, type)

    async def to_default(self, type):
        settings = await self.layer.insert_json({}, type)
        return f'⚙️ Настройки {'аккаунта' if type == 'user' else 'персонажа'}', self.IKB.setting(settings, type)

    async def to_insert_json(self, type, msg):
        await self.state.update_data(type=type, msg=msg)
        await self.state.set_state(SettingState.insert_json)
        return '✏️ Отправьте новые настройки в JSON-формате', self.IKB.back(f'{type}_setting', type)

    async def insert_json(self, json_data: str):
        type = await self.state.get_value('type')
        try:
            data = json.loads(json_data.replace("'", '"').replace('True', 'true').replace('False', 'false'))
        except:
            raise
        for k, v in data.items():
            if k not in [a.tag for a in self.paramerts.all_parameters]:
                raise SettingTagError(f'This user(tg_id={self.tg_id}) enter tag and this tag not exist')
            if v not in self.paramerts.parameters_tags.get(k).redact_values:
                raise SettingValueError(f'This user(tg_id={self.tg_id}) enter value and this value not exist')
        settings = await self.layer.insert_json(data, type)
        return f'⚙️ Настройки {'аккаунта' if type == 'user' else 'персонажа'}', self.IKB.setting(settings, type)
 
