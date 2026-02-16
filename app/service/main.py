from aiogram.fsm.context import FSMContext
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.base import UserText
from app.aio.msg.utils import TextHTML
from app.service.base import BaseService 
from app.interlayer.main import UserLayer

class UserService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = UserLayer(tg_id)

    async def get_info(self, user_id: int | None = None):
        layer = await self.layer.get_char_info()
        text = UserText(layer.user.tg_user, layer.user).text
        logs.info(text)
        return text
