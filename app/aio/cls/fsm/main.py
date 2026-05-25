from aiogram.filters.state import State, StatesGroup

class ChatState(StatesGroup):
    redact_text_parametr = State()
    chat_id: int
