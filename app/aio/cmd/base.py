from aiogram import Router, F
from app.aio.cmd.char.mychar import char_router
from app.aio.cmd.start import start_router
from app.aio.cmd.faq import faq_router
from app.aio.cmd.transfer.transfer import transfer_router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.main import UserService
from app.exeption.decorator import exept


base_router = Router()
base_router.include_routers(start_router, char_router, transfer_router, faq_router)

@base_router.message(Command('user'))
@log.decor(arg=True)
@exept
async def cmd_add_item_name(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args != None and message.from_user.id == owner:
        msg = await UserService(message.from_user.id, state).get_info(command.args)
        await message.answer(msg)
    elif message.from_user.id != owner:
        await message.answer('❌ Нет доступа')
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')


