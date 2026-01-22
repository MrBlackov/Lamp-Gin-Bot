from aiogram.filters.state import State, StatesGroup
from typing import Literal
from app.validate.sketchs.item_sketchs import ItemSketch

class AddItemState(StatesGroup):
    name: str = State()
    emoji: str
    description: str = State()
    quantity: int = State()
    msg: list = None