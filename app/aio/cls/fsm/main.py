from aiogram.filters.state import State, StatesGroup

class ChatState(StatesGroup):
    msg_delete_time = State()
    chat_id: int
