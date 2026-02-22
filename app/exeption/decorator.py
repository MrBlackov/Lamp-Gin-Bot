from functools import wraps
from aiogram.types import Message, CallbackQuery
from app.exeption.base import BotError
from app.logged.botlog import log
from app.aio.config import owner
from app.aio.inline_buttons.faq import FaqIKB

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
            markup = FaqIKB().to_error_faq(bote.code) if len(bote.faq) > 0 else None
            await message.answer(bote.to_msg, reply_markup=markup)
        except Exception as e:
            log.error(f'AioPartPath: {e}')
            if message.from_user.id == owner:
                await message.answer(f'⚠️ Непредвиденная ошибка: {e} (500.0)')
            else:
                await message.answer(f'⚠️ Непредвиденная ошибка (500.0)')
            raise e
        finally:
            await dowload.delete()
    return wrapped

def call_exept(func):
    @wraps(func)
    async def wrapped(callback: CallbackQuery, **kwargs): 
        answer_text = '⌛'
        show_alert=None
        try:
            result = await func(callback=callback, **kwargs)
            return result, callback
        except BotError as bote:
            log.warning(f'AioPartPath: {bote}')
            show_alert=True
            answer_text = bote.to_msg
        except Exception as e:
            log.error(f'AioPartPath: {e}')
            show_alert=True
            if callback.from_user.id == owner:
                answer_text = f'⚠️ Непредвиденная ошибка: {e} (500.0)'
            else:
                answer_text = f'⚠️ Непредвиденная ошибка (500.0)'
            raise e
        finally:
            try:
                await callback.answer(answer_text, show_alert=show_alert)
            except Exception as e:
                log.error(f'AioPartPath: {e}')
                if callback.from_user.id == owner:
                    await callback.message.answer(f'⚠️ {e} (500.0) \n \n {answer_text}', show_alert=True)
                else:
                    await callback.answer(f'⚠️ Непредвиденная ошибка (500.0)', show_alert=True)

    return wrapped 
