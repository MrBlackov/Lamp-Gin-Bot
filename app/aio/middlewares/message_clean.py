from aiogram.methods import SendMessage, TelegramMethod, EditMessageText
from aiogram.client.session.middlewares.base import BaseRequestMiddleware, NextRequestMiddlewareType
from app.scheduler.message import MessageUtils
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from aiogram import Bot
from app.aio.config import log_groups


class MessageCleanRequestMiddleware(BaseRequestMiddleware):
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType,
        bot: Bot,
        method: TelegramMethod[Any],
    ) -> TelegramMethod[Any]:
        
        to_msg_delete = False
        if isinstance(method, (SendMessage, EditMessageText)):
            to_msg_delete = True

        result = await make_request(bot, method)
        
        # Анализируем результат после отправки
        if to_msg_delete and hasattr(result, 'message_id') and hasattr(result, 'chat') and hasattr(result, 'from_user'):
            if result.from_user.is_bot and result.chat.id not in log_groups:
                await MessageUtils(result.chat.id).add_to_delete(result.message_id)
        
        return result

class MessageCleanDpMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        callback: CallbackQuery | None = data.get('callback')
        if callback:
            await MessageUtils(callback.message.chat.id).update_time_default(callback.message.message_id)

        data['utils'] = MessageUtils
        result = await handler(event, data)    
        
        return result