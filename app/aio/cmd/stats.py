from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.stats import StatsService

stats_router = Router()   

@stats_router.message(Command('stats'))
@log.decor(arg=True)
@exept
async def cmd_add_item_name(message: Message, command: CommandObject, state: FSMContext):
    if message.from_user.id == owner:
        msg = await StatsService(message.from_user.id, state).all_coins()
        await message.answer(msg)
    elif message.from_user.id != owner:
        await message.answer('❌ Нет доступа')
    else:
        await message.answer('⁉️ Неизввестная ошибка')



