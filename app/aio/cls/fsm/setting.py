from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class SettingState(StatesGroup):
    insert_json = State()
    type: str


