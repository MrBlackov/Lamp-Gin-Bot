from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.setting import SettingFSM, SettingService, SettingState
from app.aio.cls.callback.setting import SettingActionCall, SettingBackCall, SettingRedactCall, MenuCall

setting_router = Router()

@setting_router.message(Command('setting'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await SettingService(message.from_user.id, state, message).get_user_setting('user')
    await message.answer(msg, reply_markup=markup)

@setting_router.callback_query(SettingBackCall.filter(F.where == 'user_setting'))     
@setting_router.callback_query(MenuCall.filter(F.where == 'user_setting'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SettingBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await SettingService(callback.from_user.id, state, callback.message).get_user_setting('user')
    await callback.message.edit_text(msg, reply_markup=markup)
    
@setting_router.callback_query(MenuCall.filter(F.where == 'char_setting'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SettingBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await SettingService(callback.from_user.id, state, callback.message).get_user_setting('char')
    await callback.message.edit_text(msg, reply_markup=markup)

@setting_router.callback_query(SettingRedactCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SettingRedactCall, state: FSMContext, **kwargs):
    msg, markup = await SettingService(callback.from_user.id, state, callback.message).redact_setting(callback_data.tag, callback_data.type)
    await callback.message.edit_text(msg, reply_markup=markup)

@setting_router.callback_query(SettingActionCall.filter(F.to_default_values == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await SettingService(callback.from_user.id, state, callback.message).to_default(callback_data.type)
    await callback.message.edit_text(msg, reply_markup=markup)

@setting_router.callback_query(SettingActionCall.filter(F.to_insert_json == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await SettingService(callback.from_user.id, state, callback.message).to_insert_json(callback_data.type, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@setting_router.message(SettingState.insert_json)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = SettingFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await SettingService(message.from_user.id, state, message).insert_json(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()
