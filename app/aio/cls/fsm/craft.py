from aiogram.filters.state import State, StatesGroup

class CraftState(StatesGroup):
    crafts: list
    page: int = 0
    back_where: str
    pages: list