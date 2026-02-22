from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class NewItemState(StatesGroup):
    to_redact = State()
    to_name = State()
    to_emodzi = State()
    sketcch: dict
    redact_key: str
    is_redact: bool = False

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

class ChangeItemSketchState(StatesGroup):
    msg: Message
    page = 0
    pages: list
    datas: dict
    items: dict[int, dict]
    what_change: str
    new_data = State()
    item_id: int
    action: str
    action_data = State()
    sketch_id: int
