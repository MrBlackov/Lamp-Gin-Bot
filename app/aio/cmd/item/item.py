from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.aio.cmd.item.admin_item import add_item_router
from app.exeption.decorator import exept

item_router = Router()
item_router.include_router(add_item_router)

@item_router.message(Command('yjddd'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, command: CommandObject):
    await message.answer('kf')
    