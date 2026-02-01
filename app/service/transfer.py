from app.service.base import BaseService
from app.interlayer.item import ItemLayer
from aiogram.types import Document
from app.aio.config import bot
from app.service.utils import str_to_json
from app.logic.query import LetterSearch


class TransferService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        
    def new_transfer(self):
        return