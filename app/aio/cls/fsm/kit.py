from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class KitState(StatesGroup):
    kits = None
    no_hide = None
    code = State()
    msg = None


