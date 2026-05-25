from app.aio.cls.callback.base import BaseCall, MenuCall

class ChatSettingActionCall(BaseCall, prefix='chat_setting_action'):
    chat_id: int
    bool_parametrs: bool | None = None
    parametrs: str 
    to_redact_text_parametr: bool | None = None
    to_redact_bool_parametr: bool | None = None

class ChatBackCall(BaseCall, prefix='chat_back'):
    where: str
