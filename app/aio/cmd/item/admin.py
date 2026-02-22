from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.item import ItemService
from app.exeption.decorator import exept

add_item_router = Router()


@add_item_router.message(Command('additem'), F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_add_item_name(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args != None and message.from_user.id == owner:
        msg = await ItemService(message.from_user.id).add.add_data_item(command.args)
        await message.answer(msg)
    elif message.from_user.id != owner:
        await message.answer('❌ Нет доступа')
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')

@add_item_router.message(Command('giveitem'))
@log.decor(arg=True)
@exept
async def cmd_add_item_name(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args != None and message.from_user.id == owner:
        msg = await ItemService(message.from_user.id).give.give(command.args)
        await message.answer(msg)
    elif message.from_user.id != owner:
        await message.answer('❌ Нет доступа')
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')
     