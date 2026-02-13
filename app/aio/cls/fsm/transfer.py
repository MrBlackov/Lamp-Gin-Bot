from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

class ItemTransferState(StatesGroup):
    search_char: str = State()
    chars: dict
    char_pages: list
    charpage: int = 0
    itempage: int = 0
    char1 = None
    char2 = None
    items1: dict[int, dict[str]] = None
    items2: dict[int, dict[str]] = None
    back_where = 'cmd'
    items = None
    side = None
    items_pages = None
    items_dict = None
    item_quantity = State()
    item_id: int = None
    action = None
    msg = None
