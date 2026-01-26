from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class AddItemState(StatesGroup):
    name: str = State()
    description: str = State()
    image: int = State()

class AddDataItemState(StatesGroup):
    data: dict = State()
    image: int = State()
    msg: Message

