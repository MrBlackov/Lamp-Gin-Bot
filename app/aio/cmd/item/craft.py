from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import admins
from app.exeption.decorator import exept, call_exept
from app.service.craft import CraftService
from app.aio.cls.callback.craft import CraftBackCall, CraftIdCall, CraftPageCall, CraftActionCall, CraftActionHidenCall

craft_router = Router()

@craft_router.message(Command('craft'))
@log.decor(arg=True)
@exept
async def cmd_new_char(message: Message, state: FSMContext):
    markup, text = await CraftService(message.from_user.id, state).get_no_hide_craft()
    await message.answer(text, reply_markup=markup)

@craft_router.callback_query(CraftBackCall.filter(F.where == 'cmd'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: CraftBackCall, state: FSMContext):
    msg, markup = await CraftService(callback.from_user.id, state).get_no_hide_craft()
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftIdCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: CraftIdCall, state: FSMContext):
    msg, markup = await CraftService(callback.from_user.id, state).craft(craft_id=callback_data.craft_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftPageCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: CraftPageCall, state: FSMContext):
    msg, markup = await CraftService(callback.from_user.id, state).crafts_page(page=callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

