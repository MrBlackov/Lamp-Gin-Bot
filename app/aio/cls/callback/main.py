from app.aio.cls.callback.base import BaseCall

class ChatSettingActionCall(BaseCall, prefix='chat_setting_action'):
    to_msg_delete_time: bool = False
    is_msg_delete: bool | None = None
    chat_id: int

class ChatBackCall(BaseCall, prefix='chat_back'):
    where: str
