from app.exeption.service import ValidStrToJSONError
from app.exeption.item import ThrowAwayQuantityNoInt, ThrowAwayQuantityLessOne, ThrowAwayQuantityFloat, BotError, ItemError
from app.exeption.base import PermissionError
from app.aio.config import bot
from app.logged.botlog import log
from aiogram.exceptions import TelegramBadRequest
from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram.types.chat_member_banned import ChatMemberStatus

def str_to_json(string: str):
    if ':' not in string:
        raise ValidStrToJSONError("String hasnt ':' ")
    if "'"  in string or "\"" in string:
        string = string.replace("'", '').replace("\"", '')
    if ', 'in string:
        string = string.replace(", ", ',')
    print(string)
    if ',' in string:
        objs = string.split(',')
    else:
        objs = [string]
    
    json = {}
    for obj in objs:
        if ':' in obj:
            if obj.index(':') != 0:
                tpl = obj.split(':')
                print(tpl)
                json |= {tpl[0]: tpl[1]}

    return json

async def to_msg(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id, text)
        return True, ''
    except TelegramBadRequest as e:
        log.warning(f"Error sending message to {chat_id}: {e}")
        return False, '❌ Сообщение было не отправлено'
    except Exception as e:
        log.warning(f"Error sending message to {chat_id}: {e}")
        return False, '❌ Сообщение было не отправлено'

def is_natural_int(string: str | None, 
                   tg_id: int | None = None, 
                   error_less_one = ThrowAwayQuantityLessOne,
                   error_float = ThrowAwayQuantityFloat,
                   error_no_int = ThrowAwayQuantityNoInt,
                   error_group = ItemError) -> int:
    try:
        quan = float(string)
        if quan <= 0:
            raise error_less_one(f'This user(tg_id={tg_id}) enter int, but int <=0: {string}')
        if quan.is_integer() == False:
            raise error_float(f'This user(tg_id={tg_id}) enter float')
        return int(quan)
    except ValueError:
        raise error_no_int(f'This user(tg_id={tg_id}) enter no int')
    except BotError:
        raise 
    except Exception as e:
        raise error_group(f'This user(tg_id={tg_id}) use exeption: {e}')

def permisiion_check(is_callback: bool, to_raise: bool = False):
    def decorator(func):
        if is_callback:
            @wraps(func)
            async def wrapped(callback: CallbackQuery, **kwargs): 
                if callback.message.chat.type in ['group', 'supergroup', 'channel']:
                    member = await bot.get_chat_member(callback.message.chat.id, callback.from_user.id)
                    if member.status != ChatMemberStatus.CREATOR:
                        if to_raise:
                            raise PermissionError(f'У пользователя(tg_id={callback.from_user.id}) нет прав для использования этой команды')
                        return
                return await func(callback, **kwargs)
            return wrapped
        @wraps(func)
        async def wrapped(message: Message, **kwargs): 
            if message.chat.type in ['group', 'supergroup', 'channel']:
                member = await bot.get_chat_member(message.chat.id, message.from_user.id)
                if member.status != ChatMemberStatus.CREATOR:
                    if to_raise:
                        raise PermissionError(f'У пользователя(tg_id={message.from_user.id}) нет прав для использования этой команды')
                    return
            return await func(message, **kwargs)       
        return wrapped
    return decorator