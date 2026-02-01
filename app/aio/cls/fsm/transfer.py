from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class ItemTransferState(StatesGroup):
    search_char: str = State()
    chars: dict

