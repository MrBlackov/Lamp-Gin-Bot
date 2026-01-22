from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import BotIKB
from app.logged.botlog import logs

class BaseService:
    def __init__(self, tg_id: int, state: FSMContext | None = None):
        self.tg_id = tg_id
        self.state = state
        self.IKB = BotIKB()


