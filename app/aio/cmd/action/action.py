from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.action import ActionService, ActionFSM, ActionSelf
from app.aio.cls.callback.action import ActionBackCall, ActionCall, MenuCall, ActionRedactCall, LookAroundCall
from app.aio.cls.fsm.action import ActionState
from app.service.utils import is_natural_int
from app.exeption.action import ActionError, ActionQuantityFloat, ActionQuantityLessOne, ActionQuantityNoInt, NotNewStatsError
from aiogram.exceptions import TelegramBadRequest

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
    msg, markup = await ActionService(callback.from_user.id, state).to_action(callback_data.tag, callback_data.step, callback_data.minute)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ActionRedactCall.filter(F.to_time == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state).to_time_redact(callback_data.tag, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.minute, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    quan = is_natural_int(message.text, message.from_user.id, ActionQuantityLessOne, ActionQuantityFloat, ActionQuantityNoInt, ActionError)
    msg, markup = await ActionService(message.from_user.id, state).time_redact(quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@action_router.callback_query(ActionRedactCall.filter(F.to_del_timer == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    try:
        msg, markup = await ActionService(callback.from_user.id, state).del_timer(callback_data.tag)
        await callback.message.edit_text(msg, reply_markup=markup)
    except TelegramBadRequest:
        raise NotNewStatsError('❌ Обновлений нету', level='debug')
    
@action_router.callback_query(ActionRedactCall.filter(F.to_stats == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    try:
        msg, markup = await ActionService(callback.from_user.id, state).to_stats(callback_data.tag)
        await callback.message.edit_text(msg, reply_markup=markup)
    except TelegramBadRequest:
        raise NotNewStatsError('❌ Обновлений нету', level='debug')

@action_router.callback_query(LookAroundCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: LookAroundCall, state: FSMContext, **kwargs):
    await callback.answer('❌ Ваших навыков недостаточно, чтобы увидеть все', show_alert=True)


for action in ActionSelf.cmd_actions:
    for prefix, cmd in action.commands().items():
        @action_router.message(Command(*cmd, prefix=prefix))
        @log.decor(arg=True)
        @exept
        async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
            print(command.command, command.args)
            msg, markup = await ActionService(message.from_user.id, state).cmd_action(command.prefix + command.command, command.args)
            await message.answer(msg, reply_markup=markup)



