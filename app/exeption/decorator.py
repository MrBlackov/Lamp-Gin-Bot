from functools import wraps
from aiogram.types import Message, CallbackQuery
from app.exeption.base import BotError, ALienCallbackError
from app.logged.botlog import log
from app.aio.config import owner
from app.aio.inline_buttons.faq import FaqIKB
from app.aio.msg.utils import TextHTML
from app.aio.cls.callback.base import BaseCall, MenuCall
import random
from aiogram.exceptions import TelegramBadRequest

def exept(func):
    @wraps(func)
    async def wrapped(message: Message, **kwargs): 
        dowload = await message.answer('⏳')
        try:
            result = await func(message, **kwargs)
            try:
                await message.delete()
            except:
                pass
            return result
        except BotError as bote:
            log.warning(f'AioPartPath: {bote}')
            markup = FaqIKB(message.from_user.id).to_error_faq(bote.code) if len(bote.faq) > 0 else None
            await message.answer((TextHTML(bote.to_msg).escape())[:4000], reply_markup=markup)
        except TelegramBadRequest as e:
            log.error(f'AioPartPath: {e}')
        except Exception as e:
            str_e = str(e)
            log.error(f'AioPartPath: {e}')
            if message.from_user.id == owner:
                await message.answer(f'⚠️ Непредвиденная ошибка: {(TextHTML(str_e).escape())[:4000]} (500.0)')
            else:
                await message.answer(f'⚠️ Непредвиденная ошибка (500.0)')
            raise e
        finally:
            await dowload.delete()
    return wrapped

def call_exept(check_is_user: bool = True, tips: list[str] | None = None, rarity_tips: float | None = None):
    def decor(func):
        @wraps(func)
        async def wrapped(callback: CallbackQuery, callback_data: BaseCall, **kwargs): 
            try:
                if check_is_user and callback_data.is_check:
                    if callback.from_user.id != callback_data.tg_id:
                        raise ALienCallbackError(f'This user(tg_id={callback.from_user.id}) enter is alien callback keyboard')
                answer_text = ''
                show_alert=None
                result = await func(callback, callback_data, **kwargs)
                if tips and rarity_tips:
                    if rarity_tips <= random.random():
                        await callback.answer(random.choice(tips))
                return result, callback
            except BotError as bote:
                log.warning(f'AioPartPath: {bote}')
                show_alert=True
                answer_text = (TextHTML(bote.to_msg).escape())[:4000]
            except TelegramBadRequest as e:
                log.error(f'AioPartPath: {e}')
            except Exception as e:
                str_e = str(e)
                log.error(f'AioPartPath: {e}')
                show_alert=True
                if callback.from_user.id == owner:
                    answer_text = f'⚠️ Непредвиденная ошибка: {(TextHTML(str_e).escape())[:4000]} (500.0)'
                else:
                    answer_text = f'⚠️ Непредвиденная ошибка (500.0)'
                raise e
            finally:
                try:
                    await callback.answer(answer_text, show_alert=show_alert)
                except Exception as e:
                    log.error(f'AioPartPath: {e}')
                    if callback.from_user.id == owner:
                        await callback.message.answer(f'⚠️ {(TextHTML(e).escape())[:4000]} (500.0) \n \n {answer_text}')
                    else:
                        await callback.answer(f'⚠️ Непредвиденная ошибка (500.0)', show_alert=True)
    
        return wrapped 
    return decor