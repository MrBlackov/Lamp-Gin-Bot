from loguru import logger
from typing import Literal
import asyncio
from app.aio.config import bot
from aiogram.types import FSInputFile
import html
import sys
from functools import wraps
from time import time
from pathlib import Path
import zipfile
import inspect

_STOP_SIGNAL = object()

def filter_by_filepath(file_path: str):
    def filter_func(record):
        if '/' in file_path:
            record_str = str(record['extra'])
            return file_path in record_str or file_path.replace('/', '') in record_str
        return False
    return filter_func

class BotLog:
    # Константы логирования
    LOG_FILE_PATH = 'app/logged/file.txt'
    LOGS_DIR = 'files/logs'
    MSG_SIZE_LIMIT = 4000
    # Лимиты Telegram API
    TG_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    TG_RATE_LIMIT_DELAY = 0.05  # 20 запросов в секунду (консервативно)
    
    # Маппинги для быстрого доступа
    _LEVEL_MAP = {
        50: ['CRITICAL.log'],
        40: ['ERROR.log'],
        30: ['WARNING.log'],
        25: ['SUCCESS.log'],
        20: ['INFO.log'],
        10: ['DEBUG.log'],
        5: ['TRACE.log']
    }
    
    _TOPIC_LOGS_MAP = {
        'aio': 'aio.log',
        'db': 'db.log',
        'logic': 'logic.log',
        'service': 'service.log'
    }
    
    _FILE_LOGS_MAP = {
        'aio': 'aio/aio',
        'db': 'db/db',
        'logic': 'logic/logic',
        'service': 'service/service'
    }
    
    def __init__(self, chat_id: int, max_size: int = 0, timeout: int = 1, sleep_timeout: int = 20):
        self.chat_id = chat_id
        self.log = logger
        self.index = 0
        self.timeout = timeout
        self.sleep_timeout = sleep_timeout
        self._queue = asyncio.Queue(maxsize=max_size)
        self._event = asyncio.Event()
        self._closed = False
        # Кэш обратного маппинга для in_topic
        self._topic_reverse_map = {v: k for k, v in self._get_topic_logs_dict().items()}
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
            'rotation':'1 day',
            'retention':'3 days',
            'filter':filter_by_filepath(path),
            'level':'DEBUG', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True
        } for log, path  in {'bot':'/','aio/aio':'aio/','db/db':'db/','service/service':'service/', 'logic/logic':'logic/'}.items()
    ] + [
        {   
            "sink":f'files/logs/{log}.log',
            'rotation':'12 hours',
            'retention':'1 day',
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
        } for level, r in {'TRACE':1, 'DEBUG':2, 'INFO':3, 'SUCCESS':4, 'WARNING':5, 'ERROR':7, 'CRITICAL':10}.items()
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
                if len(msg) > self.MSG_SIZE_LIMIT:
                    with open(self.LOG_FILE_PATH, 'w', encoding='utf-8') as file:
                        file.writelines([html.unescape(m + '\n') for m in msg.split(', ')])
                    send_file = FSInputFile(self.LOG_FILE_PATH, 'message.txt')    
                    await bot.send_document(chat_id=self.chat_id, document=send_file, caption='<b>message file</b>', message_thread_id=topic_id)
                else:
                    await bot.send_message(chat_id=self.chat_id, text=msg, message_thread_id=topic_id, parse_mode='HTML')
        except Exception as e:
            await self._queue.put(item)
            print(e)
            return True
        
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


    def _get_topic_logs_dict(self) -> dict:
        return {
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
    
    def in_topic(self, key: str | int | None = None):
        topic_logs = self._get_topic_logs_dict()
        if isinstance(key, int):
            return topic_logs.get(key, 137)
        elif isinstance(key, str):
            return self._topic_reverse_map.get(key, 137)
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
    
    
        if len(to_msg) > self.MSG_SIZE_LIMIT:
            list_msg = to_msg.split('<k> ')
            list_path_msg = []
            return_msg = []
            char_count = 0
            for msg in list_msg:
                char_count += len(msg)
                if len(msg) > self.MSG_SIZE_LIMIT or char_count > self.MSG_SIZE_LIMIT:
                    if list_path_msg:
                        return_msg.append('\n'.join(list_path_msg))
                        list_path_msg = []
                        char_count = 0
                    return_msg.append(msg)
                else:
                    list_path_msg.append(msg)
            
            if list_path_msg:
                return_msg.append('\n'.join(list_path_msg))
        else:
            return_msg = [to_msg.replace('<k> ', '')]
    
    
        return return_msg   

    def to_topic_level(self, level: int):
        return self._LEVEL_MAP.get(level, [])       
    
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

    def _get_module_category(self, func) -> str:
        path = str(func.__module__).split('.')
        for category in self._TOPIC_LOGS_MAP.keys():
            if category in path:
                return category
        return None
    
    def in_file_logs(self, func):
        category = self._get_module_category(func)
        return [self._FILE_LOGS_MAP[category]] if category else []
            
    def in_topics_logs(self, func):
        category = self._get_module_category(func)
        return [self._TOPIC_LOGS_MAP[category]] if category else []  
    
    def decor(self, timer: bool = False, arg: bool = False):
        def decorator(func):
            is_async = inspect.iscoroutinefunction(func)
            
            if is_async:
                @wraps(func)
                async def async_wrapped(*args, **kwargs):
                    topic = self.in_topics_logs(func)
                    logs = self.log.bind(topics_id=topic)
                    start_time = time()
                    try:
                        if arg:
                            logs.debug(f"args: {args}, kwargs: {kwargs}")
                        else:
                            logs.trace(f"args: {args}, kwargs: {kwargs}")
                        
                        result = await func(*args, **kwargs)
                        end_time = time()
                        
                        log_method = logs.debug if timer else logs.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        return result
                    except Exception as e:
                        logs.exception(e)
                        raise
                return async_wrapped
            else:
                @wraps(func)
                def sync_wrapped(*args, **kwargs):
                    topic = self.in_topics_logs(func)
                    logs = self.log.bind(topics_id=topic)
                    start_time = time()
                    try:
                        if arg:
                            logs.debug(f"args: {args}, kwargs: {kwargs}")
                        else:
                            logs.trace(f"args: {args}, kwargs: {kwargs}")
                        
                        result = func(*args, **kwargs)
                        end_time = time()
                        
                        log_method = logs.debug if timer else logs.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        return result
                    except Exception as e:
                        logs.exception(e)
                        raise
                return sync_wrapped
        return decorator

    def __getattr__(self, name: str):
        """Динамическая делегация методов логирования"""
        if name in ('trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'):
            return getattr(self.log, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    async def news(self, msg: str, nowait: bool = False, level: Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'] = 'TRACE'):
        level = level.lower()
        method_log = getattr(self, level)
        method_log(msg)
        logs = tuple([msg, self.in_topic(level + '.log')])
        if nowait: 
            self.put_nowait(logs)
        else:
            await self.put(logs)
    
    async def send_log_file(self, log_name: str, caption: str = None):
        """Отправляет файл лога в Telegram с проверкой лимитов
        
        Args:
            log_name: имя файла лога (напр. 'bot.log', 'ERROR.log')
            caption: описание файла (опционально)
        
        Returns:
            bool: успешность отправки
        """
        log_path = Path(self.LOGS_DIR) / log_name
        if not log_path.exists():
            print(f"🗂️ Log file not found: {log_path}")
            return False
        
        file_size = log_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        # Проверка размера файла
        if file_size > self.TG_MAX_FILE_SIZE:
            print(f"🗂️ Log file {log_name} is {file_size_mb:.2f}MB, exceeds 50MB limit. Archiving...")
            return await self._send_archived_log(log_path, file_size_mb, caption)
        
        try:
            send_file = FSInputFile(str(log_path), log_name)
            await bot.send_document(
                chat_id=self.chat_id,
                document=send_file,
                caption=caption or f'📋 {log_name} ({file_size_mb:.2f}MB)',
                message_thread_id=177015
            )
            print(f"🗂️ Sent log file {log_name} ({file_size_mb:.2f}MB)")
            return True
        except Exception as e:
            print(f"🗂️ Failed to send log file {log_name}: {e}")
            return False
    
    async def _send_archived_log(self, log_path: Path, file_size_mb: float, caption: str = None):
        """Архивирует и отправляет большой лог"""
        try:
            archive_name = log_path.stem + '_archive.zip'
            archive_path = log_path.parent / archive_name
            
            # Архивирование
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(log_path, arcname=log_path.name)
            
            archive_size_mb = archive_path.stat().st_size / (1024 * 1024)
            
            if archive_path.stat().st_size > self.TG_MAX_FILE_SIZE:
                print(f"🗂️ Archived log still exceeds 50MB ({archive_size_mb:.2f}MB)")
                archive_path.unlink()  # Удаляем архив
                return False
            
            send_file = FSInputFile(str(archive_path), archive_name)
            await bot.send_document(
                chat_id=self.chat_id,
                document=send_file,
                caption=caption or f'📦 {log_path.name} (compressed: {archive_size_mb:.2f}MB from {file_size_mb:.2f}MB)',
                message_thread_id=177015
            )
            print(f"🗂️ Sent archived log {archive_name} ({archive_size_mb:.2f}MB)")
            archive_path.unlink()  # Удаляем архив после отправки
            return True
        except Exception as e:
            self.error(f"Failed to send archived log: {e}")
            return False
    
    async def send_all_log_files(self, delay: bool = True):
        """Отправляет все файлы логов в Telegram с соблюдением rate limits
        
        Args:
            delay: добавлять ли задержку между отправками (для соблюдения лимитов)
        
        Returns:
            tuple: (отправлено, всего, Message)
        """
        msg = None
        logs_dir = Path(self.LOGS_DIR)
        if not logs_dir.exists():
            print(f"🗂️ Logs directory not found: {logs_dir}")
            return 0, 0
        
        log_files = sorted(logs_dir.glob('**/*.log'), key=lambda p: p.stat().st_size, reverse=True)
        sent_count = 0
        failed_count = 0
        total_size = 0
        
        print(f"🗂️ Starting to send {len(log_files)} log files...")
        
        for idx, log_file in enumerate(log_files, 1):
            file_size_mb = log_file.stat().st_size / (1024 * 1024)
            total_size += log_file.stat().st_size
            relative_path = log_file.relative_to(logs_dir)
            
            try:
                # Проверка размера файла
                if log_file.stat().st_size > self.TG_MAX_FILE_SIZE:
                    print(f"🗂️ [{idx}/{len(log_files)}] File {relative_path} is {file_size_mb:.2f}MB, archiving...")
                    if await self._send_archived_log(log_file, file_size_mb):
                        sent_count += 1
                    else:
                        failed_count += 1
                else:
                    send_file = FSInputFile(str(log_file), str(relative_path))
                    msg = await bot.send_document(
                        chat_id=self.chat_id,
                        document=send_file,
                        caption=f'[{idx}/{len(log_files)}] 📋 {relative_path} ({file_size_mb:.2f}MB)',
                        message_thread_id=177015
                    )
                    sent_count += 1
                
                # Соблюдение rate limits Telegram
                if delay and idx < len(log_files):
                    await asyncio.sleep(self.TG_RATE_LIMIT_DELAY)
                print(f"🗂️ Sent {relative_path}")
            except Exception as e:
                failed_count += 1
                print(f"🗂️ Failed to send {log_file}: {e}")
        
        total_size_mb = total_size / (1024 * 1024)
        print(f"🗂️ Completed: {sent_count} sent, {failed_count} failed, total {total_size_mb:.2f}MB")
        return sent_count, len(log_files), msg

log = BotLog(chat_id=-1003226274859, timeout=5, sleep_timeout=20).create_handlers()
logs = log.log

async def tg_log():
    async for item in log:
        try:
            item
            print('👔 Работает, ', 'Неотправленных логов:', log._queue.qsize())
            await asyncio.sleep(log.timeout)
        except Exception as e:
            print(e)  
            await asyncio.sleep(log.sleep_timeout)
            return True
        