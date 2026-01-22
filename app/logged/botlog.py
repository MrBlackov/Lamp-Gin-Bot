from loguru import logger
from typing import Literal
import asyncio
from app.aio.config import bot
from aiogram.types import FSInputFile
import html
import sys
from functools import wraps
from time import time
import html

_STOP_SIGNAL = object()

def filter_by_filepath(file_path: str):
    def filter_func(record):
        if '/' in file_path:
            if file_path in str(record['extra']):
                return True
            elif file_path.replace('/', '') in str(record['extra']):
                return True
            else:
                False
    return filter_func

class BotLog:
    
    def __init__(self, chat_id: int, max_size: int = 100, timeout: int = 1, sleep_timeout: int = 20):
        self.chat_id = chat_id
        self.log = logger
        self.index = 0
        self.timeout = timeout
        self.sleep_timeout = sleep_timeout
        self._queue = asyncio.Queue(maxsize=max_size)
        self._event = asyncio.Event()
        self._closed = False
        self.log_format = log_format = """{level.icon}  | <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <magenta>{file}/{function}/{line}</magenta>
 >   <yellow>({process.id} - {process.name})</yellow> ~~ <yellow>({thread.id} - {thread.name})</yellow>
 >   <blue>[{extra}]</blue>
 >   <red>{exception}</red>
 >   {name}:  <cyan>{message}</cyan>\n"""
    
        self.sinks = self.handlers()

    def handlers(self):
        sinks = [{
            'sink':self.to_telegarm,
            'level':'DEBUG',
        },{
            'sink':sys.stderr,
            'level':'DEBUG',
            'format':self.log_format,
            'enqueue':True,
        }
    ] + [
        {   
            "sink":f'files/logs/{log}.log',
            'rotation':'1 week',
            'retention':'15 days',
            'filter':filter_by_filepath(path),
            'level':'DEBUG', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True
        } for log, path  in {'bot':'/','aio/aio':'aio/','db/db':'db/','service/service':'service/', 'logic/logic':'logic/'}.items()
    ] + [
        {   
            "sink":f'files/logs/{log}.log',
            'rotation':'1 day',
            'retention':'2 days',
            'filter':filter_by_filepath(path),
            'level':'TRACE', 
            'enqueue':True,
            'format':self.log_format
        } for log, path  in {'bot':'/','aio/trace':'aio/','db/trace':'db/','service/trace':'service/', 'logic/trace':'logic/'}.items()
    ] + [
        {
            "sink":f'files/logs/levels/{level}.log',
            'rotation':f'{r} days',
            'retention':f'{r*3} days',
            'level':f'{level}', 
            'enqueue':True,
            'format':self.log_format
        }  for level, r in {'TRACE':2, 'DEBUG':5, 'INFO':7, 'SUCCESS':10, 'WARNING':12, 'ERROR':15, 'CRITICAL':20}.items()
    ]
        
        return sinks
 
    def create_handlers(self):
        logger.remove()
        id_handlers = []
        for handler in self.sinks:
            l = logger.add(**handler)
            id_handlers.append(l)
        
        self.log = logger.bind(topic_id=['bot.log'], topics_id=[],)
        return self

    def __aiter__(self):
        self.index += 1
        return self

    async def __anext__(self):
        if self._closed and self._queue.empty():
            return

        item = await self._queue.get()

        if item is _STOP_SIGNAL:
            await self._queue.put(item)
            return
        
        msg_list, topic_id = item
        
        try:
            for msg in reversed(msg_list):

                if len(msg) > 4000: 
                    with open('app/logged/file.txt', 'w', encoding='utf-8') as file:
                        file.writelines([html.unescape(m + '\n') for m in msg.split(', ')])
                    send_file = FSInputFile('app/logged/file.txt', 'message.txt')    
                    await bot.send_document(chat_id=self.chat_id, document=send_file, caption='<b>message file</b>', message_thread_id=topic_id)
                    continue
                else:
                    await bot.send_message(chat_id=self.chat_id, text=msg, message_thread_id=topic_id, parse_mode='HTML')
        except Exception as e:
            await self._queue.put(item)
            print(e)
            raise e
        
        return item

    async def put(self, item):
        if self._closed:
            raise RuntimeError('Итератор закрыт')
        
        await self._queue.put(item)

    def put_nowait(self, item):
        if self._closed:
            raise RuntimeError('Итератор закрыт')
        
        self._queue.put_nowait(item)   

    async def stop(self):
        self._closed = True
        await self._queue.put(_STOP_SIGNAL)


    def in_topic(self, key: str | int | None = None):
        topic_logs = {
                6: 'bot.log',
                10: 'aio.log',
                14: 'db.log',
                18: 'TRACE.log',
                22: 'DEBUG.log',
                26: 'INFO.log',
                30: 'SUCCESS.log',
                34: 'WARNING.log',
                38: 'ERROR.log',
                42: 'CRITICAL.log',
                48: 'service.log'

            }    
        if type(key) == int:
            if key in topic_logs.keys():
               return topic_logs[key]
            else:
               return 137
        elif type(key) == str:
            return {v:k for k,v in topic_logs.items()}[key]
        else:
            return topic_logs
    
    def to_log_msg(self, record):
        to_msg = f"""<b>level</b>: {record['level'].icon} - {record['level'].name}
<b>time</b>: {record['time'].date()} {record['time'].time()}
<b>exception</b>: {html.escape(str(record['exception']))}
<b>filename</b>: {record['file']}
<b>func</b>: {record['function']}
<b>line</b>: {record['line']}
<b>process</b>: {record['process'].id} - {record['process'].name}
<b>thread</b>: {record['thread'].id} - {record['thread'].name} 
<k> <b>extra</b>: <blockquote expandable>{html.escape(str(record['extra']))} </blockquote>
<k> <b>message</b>: <blockquote expandable>{html.escape(str(record['message']))} </blockquote>
<k> 
#date_{str(record['time'].date()).replace('-', '_')}  #{record['level'].name} #{record['function']} #{record['module']} 
"""
    
    
        if len(to_msg) > 4000:
            list_msg = to_msg.split('<k> ')
            list_path_msg = []
            return_msg = []
            simvols = 0
            for msg in list_msg:
                simvols += len(msg)
                if len(msg) > 4000 or simvols > 4000:
                    return_msg.append(msg)
                    simvols -= len(msg)
                else:
                    list_path_msg.append(msg) 
                
            
            return_msg.append('\n'.join(list_path_msg))
        else:
            return_msg = [to_msg.replace('<k> ', '')]
    
    
        return return_msg   

    def to_topic_level(self, level: int):
        match level:
            case 50:
                return ['CRITICAL.log']
            case 40:
                return ['ERROR.log']
            case 30:
                return ['WARNING.log']
            case 25:
                return ['SUCCESS.log']
            case 20:
                return ['INFO.log']
            case 10:
                return ['DEBUG.log']        
            case 5:
                return ['TRACE.log'] 
            case _:
                return []       
    
    async def to_telegarm(self, log):
        record = log.record
         
        list_msg = self.to_log_msg(record)
        level_topic = self.to_topic_level(record['level'].no)
        topic_ids = record['extra']['topics_id']+level_topic+record['extra']['topic_id']
    
        for topic_id in topic_ids:
            print(topic_id)
            if record['level'].no >= 40:
                self.put_nowait((list_msg, self.in_topic(topic_id)))
                continue
    
            await self.put((list_msg, self.in_topic(topic_id)))  

    def in_file_logs(self, func):
        path = str(func.__module__).split('.')
        if 'aio' in path:
                return ['aio/aio']
        elif 'db' in path:
                return ['db/db']        
        elif 'logic' in path:
                return ['logic/logic']     
        elif 'service' in path:
                return ['service/service']          
        return []
            
    def in_topics_logs(self, func):
        path = str(func.__module__).split('.')
        if 'aio' in path:
                return ['aio.log']
        elif 'db' in path:
                return ['db.log']    
        elif 'logic' in path:
                return ['logic.log']       
        elif 'service' in path:
                return ['service.log']     
        return []  
    
    def decor(self, timer: bool = False, arg: bool = False):
        def decorator(func):
            @wraps(func)    
            def wrapped(*args, **kwargs):
                try:   
                    topic = self.in_topics_logs(func)
        
                    start_time = time()
                    logs = self.log.bind(topics_id=topic)
                    result = func(*args, **kwargs)
                    end_time = time()   
                    if arg == True:
                        logs.debug(f"args: {args}, kwargs: {kwargs}") 
                    else:    
                        logs.trace(f"args: {args}, kwargs: {kwargs}") 
                    if timer == True:
                        logs.debug(f"Функция {func.__name__} выполнена за {end_time - start_time}")  
                    else:  
                        logs.trace(f"Функция {func.__name__} выполнена за {end_time - start_time}")        
                    return result
                except Exception as e:
                    logs.exception(e)
                    raise e
        
            return wrapped
        return decorator

    def trace(self, msg: str, *args, **kwargs):
        self.log.trace(msg, *args, **kwargs)
  
    def debug(self, msg: str, *args, **kwargs):
        self.log.debug(msg, *args, **kwargs)
      
    def success(self, msg: str, *args, **kwargs):
        self.log.success(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.log.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        self.log.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        self.log.critical(msg, *args, **kwargs)

    async def news(self, msg: str, nowait: bool = False, level: Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'] = 'TRACE'):
        level = level.lower()
        method_log = getattr(self, level)
        method_log(msg)
        logs = tuple([msg, self.in_topic(level + '.log')])
        if nowait: 
            await self.put_nowait(logs)
        else:
            await self.put(logs)

log = BotLog(chat_id=-1003226274859, timeout=5, sleep_timeout=20).create_handlers()
logs = log.log

async def tg_log():
    async for item in log:
        try:
            item
            print('Работает, ', 'Неотправленных логов:', log._queue.qsize())
            await asyncio.sleep(log.timeout)
        except Exception as e:
            print(e)  
            await asyncio.sleep(log.sleep_timeout)
        