from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from app.logged.botlog import log
from app.aio.config import bot
from app.service.main import ChatService
from app.exeption.decorator import exept, call_exept
from app.service.utils import permisiion_check
from app.aio.cls.fsm.main import ChatState
from app.aio.cls.fsm.utils import UserFSM, ChatFSM
from app.aio.cls.callback.main import ChatSettingActionCall, ChatBackCall
from aiogram.types.chat_member_banned import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

chat_router = Router()

@chat_router.message(Command('chat'), F.chat.type.in_(['group', 'supergroup', 'channel']))
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await ChatService(message.from_user.id, state, message).menu(message.chat.id)
    await message.answer(msg, reply_markup=markup)

@chat_router.message(Command('chat'))
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await ChatService(message.from_user.id, state, message).menu(message.chat.id)
    await message.answer(msg, reply_markup=markup)

@chat_router.callback_query(ChatBackCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatBackCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state, callback.message).menu(callback.message.chat.id)
    await callback.message.edit_text(msg, reply_markup=markup)

@chat_router.callback_query(ChatSettingActionCall.filter(F.to_redact_text_parametr == True))     
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatSettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state, callback.message).redact_text_parametrs(callback_data.chat_id, callback_data.parametrs, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@chat_router.message(ChatState.redact_text_parametr, F.content_type == 'text', F.text.not_contains('/'))
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ChatFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ChatService(message.from_user.id, state, message).new_msg_delete_time(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@chat_router.callback_query(ChatSettingActionCall.filter(F.parametrs != None))   
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatSettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state, callback.message).redact_is_bool_parametrs(callback_data.chat_id, callback_data.bool_parametrs, callback_data.parametrs)
    await callback.message.edit_text(msg, reply_markup=markup)

@chat_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def welcome_new_member(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    full_name = user.full_name or "Пользователь"
    await ChatService(event.from_user.id).send_greetings_new_member(event.chat.id, full_name)

@chat_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def goodbye_member(event: ChatMemberUpdated):
    user = event.old_chat_member.user
    full_name = user.full_name or "Пользователь"
    await ChatService(event.from_user.id).send_greetings_new_member(event.chat.id, full_name)