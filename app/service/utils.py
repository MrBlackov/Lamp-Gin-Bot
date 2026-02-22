from app.exeption.service import ValidStrToJSONError
from app.exeption.item import ThrowAwayQuantityNoInt, ThrowAwayQuantityLessOne, ThrowAwayQuantityFloat, BotError, ItemError
from app.aio.config import bot
from app.logged.botlog import log
from aiogram.exceptions import TelegramBadRequest

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

def is_natural_int(string: str | None, tg_id: int | None = None) -> int:
    try:
        quan = float(string)
        if quan <= 0:
            raise ThrowAwayQuantityLessOne(f'This user(tg_id={tg_id}) enter int, but int <=0: {string}')
        if quan.is_integer() == False:
            raise ThrowAwayQuantityFloat(f'This user(tg_id={tg_id}) enter float')
        return int(quan)
    except ValueError:
        raise ThrowAwayQuantityNoInt(f'This user(tg_id={tg_id}) enter no int')
    except BotError:
        raise 
    except Exception as e:
        raise ItemError(f'This user(tg_id={tg_id}) use exeption: {e}')
