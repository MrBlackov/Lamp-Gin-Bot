from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import bot
from app.service.main import ChatService
from app.exeption.decorator import exept, call_exept
from app.service.utils import is_natural_int, permisiion_check
from app.aio.cls.fsm.main import ChatState
from app.aio.cls.fsm.utils import UserFSM, ChatFSM
from app.aio.cls.callback.main import ChatSettingActionCall, ChatBackCall
from app.exeption.main import MainQuantityFloat, MainQuantityLessSixTeen, MainQuantityNoInt
from aiogram.types.chat_member_banned import ChatMemberStatus

chat_router = Router()

@chat_router.message(Command('chat'), F.chat.type.in_(['group', 'supergroup', 'channel']))
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await ChatService(message.from_user.id, state).menu(message.chat.id)
    await message.answer(msg, reply_markup=markup)

@chat_router.message(Command('chat'))
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await ChatService(message.from_user.id, state).menu(message.chat.id)
    await message.answer(msg, reply_markup=markup)

@chat_router.callback_query(ChatBackCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatBackCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state).menu(callback.message.chat.id)
    await callback.message.edit_text(msg, reply_markup=markup)

@chat_router.callback_query(ChatSettingActionCall.filter(F.to_msg_delete_time == True))     
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatSettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state).redact_msg_delete_time(callback_data.chat_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@chat_router.message(ChatState.msg_delete_time)
@log.decor(arg=True)
@exept
@permisiion_check(False)
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ChatFSM(state)
    msg0 = await fsm.get_value('msg')
    quan = is_natural_int(message.text, 
                          message.from_user.id,
                          MainQuantityLessSixTeen,
                          MainQuantityFloat,
                          MainQuantityNoInt)
    msg, markup = await ChatService(message.from_user.id, state).new_msg_delete_time(quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@chat_router.callback_query(ChatSettingActionCall.filter(F.is_msg_delete == True))   
@chat_router.callback_query(ChatSettingActionCall.filter(F.is_msg_delete == False))   
@log.decor(arg=True)
@call_exept()
@permisiion_check(True, True)
async def callback_handler(callback: CallbackQuery, callback_data: ChatSettingActionCall, state: FSMContext, **kwargs):
    msg, markup = await ChatService(callback.from_user.id, state).redact_is_msg_delete(callback_data.chat_id, callback_data.is_msg_delete)
    await callback.message.edit_text(msg, reply_markup=markup)



