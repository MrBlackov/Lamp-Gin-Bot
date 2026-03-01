from aiogram.filters.state import State, StatesGroup

class CraftState(StatesGroup):
    crafts: list
    page: int = 0
    back_where: str
    pages: list
    item_type: str
    items_pages: str
    itempage: str
    items_dict: str
    item_id: str
    
