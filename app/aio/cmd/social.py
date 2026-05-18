from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.social import SocialFSM, SocialService, SocialState
from app.aio.cls.callback.social import SocialBackCall, MenuCall, SocialActionCall, SocialFriendCall, SocialRequestCall

social_router = Router()

@social_router.message(Command('myfriends'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await SocialService(message.from_user.id, state, message).get_friends()
    await message.answer(msg, reply_markup=markup)

@social_router.callback_query(SocialBackCall.filter(F.where == 'myfriends'))     
@social_router.callback_query(MenuCall.filter(F.where == 'myfriends'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: SocialBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await SocialService(callback.from_user.id, state, callback.message).get_friends()
    await callback.message.edit_text(msg, reply_markup=markup)

@social_router.callback_query(SocialFriendCall.filter(F.to_info == True))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: SocialFriendCall, state: FSMContext, **kwargs):
    msg, markup = await SocialService(callback.from_user.id, state, callback.message).friend(callback_data.user_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@social_router.callback_query(SocialFriendCall.filter(F.to_delete == True))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: SocialFriendCall, state: FSMContext, **kwargs):
    msg, markup = await SocialService(callback.from_user.id, state, callback.message).delete_friend(callback_data.user_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@social_router.callback_query(SocialActionCall.filter(F.to_send_request == True))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: SocialActionCall, state: FSMContext, **kwargs):
    msg, markup = await SocialService(callback.from_user.id, state, callback.message).to_send_request(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@social_router.message(SocialState.friend_data)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = SocialFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await SocialService(message.from_user.id, state, message).send_request(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@social_router.callback_query(SocialRequestCall.filter())  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: SocialRequestCall, state: FSMContext, **kwargs):
    msg, markup = await SocialService(callback.from_user.id, state, callback.message).answer_request(callback_data.user_id, callback_data.status)
    await callback.message.edit_text(msg, reply_markup=markup)
    



