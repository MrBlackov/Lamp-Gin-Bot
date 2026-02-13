from aiogram import Router
from app.aio.cmd.transfer.newtransfer import new_transfer_router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept
from app.service.transfer import ItemTransferService

transfer_router = Router()
transfer_router.include_routers(new_transfer_router)


@new_transfer_router.message(Command('newtransfer'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await ItemTransferService(message.from_user.id, state).new_transfer()
    await message.answer(msg, reply_markup=markup)