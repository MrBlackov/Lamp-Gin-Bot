from aiogram.filters.state import State, StatesGroup

class AddCraftState(StatesGroup):
    page: int = 0
    back_where: str
    item_type: str
    items_pages: str
    itempage: str
    items_dict: str
    item_id: str

    results: list
    tools: list
    ingredients: list
    item_quantity: int = State()
    time: int = State()
    

class CraftState(StatesGroup):
    crafts: list
    page: int = 0
    back_where: str
    pages: list