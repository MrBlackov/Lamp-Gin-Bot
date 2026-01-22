from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Chat
from app.db.metods.adds import add_or_update_tg_chat, add_or_update_tg_user
from app.db.metods.gets import get_user_for_tg_id

class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print("Before handler")
        result = await handler(event, data)
        print("After handler")
        return result
    
class UpdateDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        datas = data['event_context']
        user: User = datas.user
        chat: Chat = datas.chat

        result = await handler(event, data)        
        await add_or_update_tg_user(data={'tg_id':user.id, 'fullname':user.full_name, 'username':user.username, 'data':user.__dict__}, tg_id=user.id)
        await get_user_for_tg_id(user.id)
        await add_or_update_tg_chat(data={'tg_id':chat.id, 'tg_type':chat.type.upper(), 'fullname':chat.full_name, 'username':chat.username, 'data':chat.__dict__}, tg_id=chat.id)

        
        return result
    


    