from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.action import ActionService, ActionFSM, ActionSelf
from app.aio.cls.callback.action import (ActionBackCall, 
                                         MenuCall, 
                                         ActionCall, 
                                         ActionRedactCall, 
                                         LookAroundCall, 
                                         ActionPageCall, 
                                         ThrowItemCall, 
                                         ThrowItemQuantityCall, 
                                         PaperCall,
                                         BookCall,
                                         BookSettingCall,
                                         RadioCall)
from app.aio.cls.fsm.action import ActionState
from app.service.utils import is_natural_int
from app.exeption.action import ActionError, ActionQuantityFloat, ActionQuantityLessOne, ActionQuantityNoInt, NotNewStatsError
from aiogram.exceptions import TelegramBadRequest

action_router = Router()

for action in ActionSelf.cmd_actions:
    for prefix, cmd in action.commands().items():
        @action_router.message(Command(*cmd, prefix=prefix))
        @log.decor(arg=True)
        @exept
        async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
            msg, markup = await ActionService(message.from_user.id, state, message).cmd_action(command.prefix + command.command, command.args, command.args)
            await message.answer(msg, reply_markup=markup)





@action_router.message(Command('actions'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await ActionService(message.from_user.id, state, message).get_actions()
    await message.answer(msg, reply_markup=markup)

@action_router.callback_query(ActionBackCall.filter(F.where == 'actions'))   
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionBackCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).get_actions(callback_data.is_details)
    await callback.message.edit_text(msg, reply_markup=markup)
      
@action_router.callback_query(MenuCall.filter(F.where == 'actions'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).get_actions()
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ActionCall.filter())     
@action_router.callback_query(BookSettingCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_action(callback_data.tag, callback_data.step, callback_data.minute, item_id=callback_data.item_id, args=callback_data.args)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ActionRedactCall.filter(F.to_time == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_time_redact(callback_data.tag, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.minute, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    quan = is_natural_int(message.text, message.from_user.id, ActionQuantityLessOne, ActionQuantityFloat, ActionQuantityNoInt, ActionError)
    msg, markup = await ActionService(message.from_user.id, state, message).time_redact(quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    if msg0:
        await msg0.delete()

@action_router.callback_query(ActionRedactCall.filter(F.to_del_timer == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    try:
        msg, markup = await ActionService(callback.from_user.id, state, callback.message).del_timer(callback_data.tag)
        await callback.message.edit_text(msg, reply_markup=markup)
    except TelegramBadRequest:
        pass
    
@action_router.callback_query(ActionRedactCall.filter(F.to_item == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    try:
        msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_item(callback_data.char_id, callback_data.tag, callback_data.item_tag, callback_data.minute)
        await callback.message.edit_text(msg, reply_markup=markup)
    except TelegramBadRequest:
        pass
    
@action_router.callback_query(ActionRedactCall.filter(F.to_stats == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionRedactCall, state: FSMContext, **kwargs):
    try:
        msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_stats(callback_data.tag)
        await callback.message.edit_text(msg, reply_markup=markup)
    except TelegramBadRequest:
        raise NotNewStatsError('❌ Обновлений нету', level='debug')

@action_router.callback_query(LookAroundCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: LookAroundCall, state: FSMContext, **kwargs):
    await callback.answer('❌ Ваших навыков недостаточно, чтобы увидеть все', show_alert=True)







@action_router.callback_query(ThrowItemCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ThrowItemCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_action(callback_data.tag, callback_data.step, callback_data.minute, item_id=callback_data.item_id, quantity=callback_data.quantity, purpose_char_id=callback_data.purpose_char_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ActionPageCall.filter(F.tag == 'throw'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ActionPageCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).char_throw(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.callback_query(ThrowItemQuantityCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: ThrowItemQuantityCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_throw_quantity(callback.message, item_id=callback_data.item_id, quantity=callback_data.quantity, purpose_char_id=callback_data.purpose_char_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.throw_quantity, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).throw_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()





@action_router.message(ActionState.dice_command, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).dice_command(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    if msg0:
        await msg0.delete()





@action_router.callback_query(PaperCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: PaperCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_action(callback_data.tag, callback_data.step, callback_data.minute, item_id=callback_data.item_id, is_escape=callback_data.is_escape, args=callback_data.args)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.redact_paper, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).redact_text('paper', 3, message.html_text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()




@action_router.callback_query(BookCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: BookCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_action(callback_data.tag, callback_data.step, callback_data.minute, item_id=callback_data.item_id, page=callback_data.page, is_escape=callback_data.is_escape, args=callback_data.args)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.book_setting, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    parametr = await fsm.get_value('parametr')
    pdict = {
        'book_name':-1,
        'book_author_name':-2,
        'book_description':-3,
    }
    msg, markup = await ActionService(message.from_user.id, state, message).redact_text('book_setting', pdict.get(parametr, 1), message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@action_router.message(ActionState.book_new_page, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).redact_text('book', 4, message.html_text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()






@action_router.callback_query(RadioCall.filter(F.micro_off == True))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: RadioCall, state: FSMContext, **kwargs):   
    radio_state = await state.get_state()
    if radio_state == 'ActionState:micro':
        await state.set_state()
        await callback.answer('✅ Микрофон выключен')
        await callback.message.edit_reply_markup()

@action_router.callback_query(RadioCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: RadioCall, state: FSMContext, **kwargs):
    msg, markup = await ActionService(callback.from_user.id, state, callback.message).to_action(callback_data.tag, callback_data.step, callback_data.minute, micro=callback_data.micro, swoo=callback_data.swoo, item_id=callback_data.item_id, args=callback_data.args)
    await callback.message.edit_text(msg, reply_markup=markup)

@action_router.message(ActionState.micro, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg1 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).redact_text('radio', 0, message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    if msg1:
        await msg1.edit_text(msg1.text)
    await fsm.update_data(msg=msg2)

@action_router.message(Command('stop'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    radio_state = await state.get_state()
    if radio_state == 'ActionState:micro':
        await state.set_state()
        await message.answer('✅ Микрофон выключен')

@action_router.message(ActionState.new_name, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ActionFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await ActionService(message.from_user.id, state, message).redact_text('tag', 2, message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()
