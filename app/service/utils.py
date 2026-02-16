from app.exeption.service import ValidStrToJSONError
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
