from aiogram.filters.callback_data import CallbackData

class ChatSettingActionCall(CallbackData, prefix='chat_setting_action'):
    to_msg_delete_time: bool = False
    is_msg_delete: bool | None = None
    chat_id: int

class ChatBackCall(CallbackData, prefix='chat_back'):
    where: str
