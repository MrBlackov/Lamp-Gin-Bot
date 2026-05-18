from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.kit import KitService
from app.exeption.decorator import exept, call_exept
from app.aio.cls.callback.kit import KitActionCall, KitBackCall, KitIdCall
from app.aio.cls.fsm.kit import KitState
from app.aio.cls.fsm.utils import KitFSM

kit_router = Router()

@kit_router.message(Command('kit'), F.text == '/kit')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await KitService(message.from_user.id, state, message).kits()
    await message.answer(msg, reply_markup=markup)

@kit_router.callback_query(KitBackCall.filter(F.where == 'cmd')) 
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: KitBackCall, state: FSMContext, **kwargs):
    msg, markup = await KitService(callback.from_user.id, state, callback.message).kits()
    await callback.message.edit_text(msg, reply_markup=markup)

@kit_router.callback_query(KitIdCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: KitIdCall, state: FSMContext, **kwargs):
    msg, markup = await KitService(callback.from_user.id, state, callback.message).kit(callback_data.kit_id, callback_data.is_new)
    await callback.message.edit_text(msg, reply_markup=markup)  
 
@kit_router.callback_query(KitActionCall.filter(F.to_enter_code == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: KitActionCall, state: FSMContext, **kwargs):
    msg, markup = await KitService(callback.from_user.id, state, callback.message).to_enter_code(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)  
 
@kit_router.message(KitState.code)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg0 = await KitFSM(state).get_value('msg')
    msg, markup = await KitService(message.from_user.id, state, message).enter_code(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

