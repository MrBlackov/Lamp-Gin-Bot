from aiogram.filters.state import State, StatesGroup
from typing import Literal

class ActionState(StatesGroup):
    tag: str
    msg = None
    minute = State()


