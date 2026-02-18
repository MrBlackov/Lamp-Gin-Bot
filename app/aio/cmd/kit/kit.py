from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.kit import KitService
from app.exeption.decorator import exept, call_exept
from app.aio.cls.callback.kit import KitActionCall, KitBackCall, KitIdCall
from app.aio.cls.fsm.kit import KitState

kit_router = Router()

@kit_router.message(Command('kit'), F.text == '/kit')
@log.decor(arg=True)
@exept
async def cmd_new_char(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await KitService(message.from_user.id, state).kits()
    await message.answer(msg, reply_markup=markup)

@kit_router.callback_query(KitBackCall.filter(F.where == 'cmd')) 
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: KitBackCall, state: FSMContext):
    await state.clear()
    msg, markup = await KitService(callback.from_user.id, state).kits()
    await callback.message.edit_text(msg, reply_markup=markup)

@kit_router.callback_query(KitIdCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: KitIdCall, state: FSMContext):
    msg, markup = await KitService(callback.from_user.id, state).kit(callback_data.kit_id, callback_data.is_new)
    await callback.message.edit_text(msg, reply_markup=markup)  
 
@kit_router.callback_query(KitActionCall.filter(F.to_enter_code == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: KitActionCall, state: FSMContext):
    msg, markup = await KitService(callback.from_user.id, state).to_enter_code(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)  
 
@kit_router.message(KitState.code)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await KitService(message.from_user.id, state).enter_code(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

