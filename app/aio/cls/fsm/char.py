from aiogram.filters.state import State, StatesGroup
from typing import Literal
from app.validate.api.characters import CharSketchInfo
from app.db.models.item import ItemDB

class CreateCharState(StatesGroup):
    gender: Literal['M', 'W'] = State()
    first_name: str = State()
    last_name: str = State()
    sketch: CharSketchInfo = State()
    description: str = State()
    to_create = State()
    fist_names: list[str]
    last_names: list[str]
    name_pages: tuple[str]
    sketchs: list[CharSketchInfo]
    free_sketchs_quantity: int
    query_value = State()
    is_first_name: bool = True
    msg = None

class InfoCharacter(StatesGroup):
    chars: dict[int, CharSketchInfo]
    main_id: int

class InventoryState(StatesGroup):
    items: dict[int, ItemDB] = State()


