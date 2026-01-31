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

class ListItemSketchsState(StatesGroup):
    sketch_ids: dict
    msg: Message
    sketches: list
    searchs: list
    name: str = State()
    page: int = 0



