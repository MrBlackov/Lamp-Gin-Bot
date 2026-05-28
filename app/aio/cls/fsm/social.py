from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class SocialState(StatesGroup):
    friend_data = State()


