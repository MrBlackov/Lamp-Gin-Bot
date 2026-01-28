from functools import wraps
from aiogram.types import Message
from app.exeption.base import BotError
from app.logged.botlog import log

def exept(func):
    @wraps(func)
    async def wrapped(message: Message, **kwargs): 
        dowload = await message.answer('⏳')
        try:
            result = await func(message=message, **kwargs)
            await message.delete()
            return result
        except BotError as bote:
            log.warning(f'AioPartPath: {bote}')
            await message.reply(bote.to_msg)
        except Exception as e:
            log.warning(f'AioPartPath: {e}')
            await message.reply('⚠️ Непредвиденная ошибка (500.0)')            
            raise e
        finally:
            await dowload.delete()
    return wrapped
