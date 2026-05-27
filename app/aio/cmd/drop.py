from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.drop import DropFSM, DropService
from app.aio.cls.callback.drop import DropBackCall, MenuCall, DropActionCall, DropItemCall

drop_router = Router()

@drop_router.message(Command('drop'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await DropService(message.from_user.id, state, message).get_drop()
    await message.answer(msg, reply_markup=markup)

@drop_router.callback_query(DropBackCall.filter(F.where == 'drop'))
@drop_router.callback_query(MenuCall.filter(F.where == 'drop'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: MenuCall, state: FSMContext, **kwargs):
    msg, markup = await DropService(callback.from_user.id, state, callback.message).get_drop()
    await callback.message.edit_text(msg, reply_markup=markup)

@drop_router.callback_query(DropActionCall.filter(F.to_open == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: DropActionCall, state: FSMContext, **kwargs):
    msg, markup = await DropService(callback.from_user.id, state, callback.message).open_drop(callback_data.drop_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@drop_router.callback_query(DropItemCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: DropItemCall, state: FSMContext, **kwargs):
    msg, markup = await DropService(callback.from_user.id, state, callback.message, callback=callback).get_item(callback_data.drop_id, callback_data.sketch_id, callback_data.quantity)
    await callback.message.edit_text(msg, reply_markup=markup)
