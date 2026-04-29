from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.action import ActionService, ActionFSM, all_action
from app.aio.cls.callback.action import ActionBackCall, ActionCall, MenuCall

action_router = Router()

@action_router.message(Command('actions'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await ActionService(message.from_user.id, state).get_actions()
    await message.answer(msg, reply_markup=markup)

@action_router.callback_query(ActionBackCall.filter(F.where == 'actions'))   
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionBackCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state).get_actions(callback_data.is_details)
    await callback.message.edit_text(msg, reply_markup=markup)
      
@action_router.callback_query(MenuCall.filter(F.where == 'actions'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state).get_actions()
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ActionCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state).to_action(callback_data.tag)
    await callback.message.edit_text(msg, reply_markup=markup)

for action in all_action:
    for prefix, cmd in action.commands().items():
        @action_router.message(Command(*cmd, prefix=prefix))
        @log.decor(arg=True)
        @exept
        async def cmd_handler(message: Message, state: FSMContext, **kwargs):
            msg, markup = await ActionService(message.from_user.id, state).cmd_action(message.text)
            await message.answer(msg, reply_markup=markup)
