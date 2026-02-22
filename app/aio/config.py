from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(config('owner'))]
owner = int(config('owner'))
newspaper_id = int(config('newcpaper_id'))
token = config('token')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
cmds = {
    'mychar':'👤 Список ваших персонажей',
    'inventory':'💼 Инвентарь',
    'transfer':'✉️ Ваши сделки',

    'newchar':'➕ Создать персонажа',
    'newtransfer':'➕ Создать сделку',
    'newitem':'➕ Создать предмет',

    'items':'📦 Список всех предметов в игре',
    'help':'📚 Получить справку',
}

admin_cmds = cmds | {
    'additem':'Добавить предмет',
    'changeitem':'Изменить предмет',
    'giveitem':'Выдать предмет',
    'user':'Посмотреть информацию о пользователе',
    'chat_id':'Получать ID чата и ID топика',
}

async def to_menu_cmds():
    admin_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in admin_cmds.items()]
    user_menu = [BotCommand(command=cmd, description=desc) for cmd, desc in cmds.items()]
    await bot.set_my_commands(admin_menu, scope=BotCommandScopeChat(chat_id=owner))
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(user_menu, scope=BotCommandScopeAllChatAdministrators())
