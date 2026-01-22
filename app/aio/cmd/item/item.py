from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.aio.cmd.item.add_item import add_item_router

item_router = Router()
item_router.include_router(add_item_router)

@item_router.message(Command('inventory'))
@log.decor(arg=True)
async def cmd_inventory(message: Message, command: CommandObject):
    await message.answer()
    