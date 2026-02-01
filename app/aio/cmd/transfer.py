from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept
from app.service.transfer import TransferService
from app.aio.cls.callback.transfer import ItemTransferCharIdCall, ItemTransferStartCall
from app.aio.cls.fsm.transfer import ItemTransferState

transfer_router = Router()

@transfer_router.message(Command('items'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await TransferService(message.from_user.id, state)
    await message.answer(msg, reply_markup=markup)

@transfer_router.callback_query(ItemTransferStartCall.filter(F.where == 'cmd'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferStartCall, state: FSMContext):
    await callback.answer()
    msg, markup = await TransferService(callback.from_user.id, state)
    await callback.message.edit_text(msg, reply_markup=markup)