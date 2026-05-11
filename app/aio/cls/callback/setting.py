from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class SettingBaseCall(BaseCall, prefix='setting_base'):
    type: str

class SettingBackCall(SettingBaseCall, prefix='setting_back'):
    where: str

class SettingRedactCall(SettingBaseCall, prefix='setting_redact'):
    tag: str

class SettingActionCall(SettingBaseCall, prefix='setting_action'):
    to_default_values: bool = False
    to_insert_json: bool = False

    