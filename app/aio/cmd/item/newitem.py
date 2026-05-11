from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import admins
from app.service.item import ItemService
from app.exeption.decorator import exept, call_exept
from app.aio.cls.fsm.item import NewItemState
from app.aio.cls.callback.item import (NewItemACtionCall, 
                                       NewItemBackCall, 
                                       NewItemAdminACtionCall,
                                       NewItemSketchDeleteActionTagCall)
from app.aio.cls.fsm.utils import ItemFSM

new_item_router = Router()


@new_item_router.message(Command('newitem'), F.text.contains('y'))
@new_item_router.message(Command('newitem'), F.text.contains('yes'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await ItemService(message.from_user.id, state).add.to_name(message)
    msg0 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg0)

@new_item_router.message(Command('newitem'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await ItemService(message.from_user.id, state).add.to_create_item()
    await message.answer(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_argree_rules == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_name(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
    await state.update_data(msg=callback.message)

@new_item_router.message(NewItemState.to_name)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.to_emodzi(message.text, message)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await msg0.delete()

@new_item_router.message(NewItemState.to_emodzi)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.to_tag(message.text, message)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await msg0.delete()


@new_item_router.message(NewItemState.to_tag)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.to_menu(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@new_item_router.callback_query(NewItemBackCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemBackCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'new').set_state()
    msg, markup = await ItemService(callback.from_user.id, state).add.menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemBackCall.filter(F.where == 'cancel'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemBackCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'new').set_state()
    await callback.message.edit_text('🙁 Создание предмета отменено', reply_markup=None)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_redact == True), NewItemACtionCall.filter(F.redact_key == 'emodzi'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_redact(callback_data.redact_key, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_redact == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_redact(callback_data.redact_key, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.message(NewItemState.to_redact)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.redact(message)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()
    
@new_item_router.callback_query(NewItemACtionCall.filter(F.to_delete_nbt == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_delete_nbt()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.delete_nbt == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.delete_nbt()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_nbt == True))    
@new_item_router.callback_query(NewItemBackCall.filter(F.where == 'nbt'))    
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'new').set_state()
    msg, markup = await ItemService(callback.from_user.id, state).add.nbt()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_action_tags == True)) 
@new_item_router.callback_query(NewItemBackCall.filter(F.where == 'action'))       
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'new').set_state()
    msg, markup = await ItemService(callback.from_user.id, state).add.to_action_tag()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_add_action == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_add_action_tag(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.message(NewItemState.add_action)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.add_action_tag(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@new_item_router.callback_query(NewItemSketchDeleteActionTagCall.filter(F.is_delete == False))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemSketchDeleteActionTagCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_delete_action_tag(callback_data.tag)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_item_router.callback_query(NewItemSketchDeleteActionTagCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemSketchDeleteActionTagCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.delete_action_tag(callback_data.tag)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_send == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_send()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_create == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.create()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.redact_item == True))     
@log.decor(arg=True)
@call_exept(False)
async def callback_handler(callback: CallbackQuery, callback_data: NewItemAdminACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).change.info(callback_data.sketch_id)
    await callback.message.answer(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_create == True))     
@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_create == False))     
@log.decor(arg=True)
@call_exept(False)
async def callback_handler(callback: CallbackQuery, callback_data: NewItemAdminACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.create_after_moderating(callback_data.sketch_id, callback_data.to_create)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_redact == False))     
@log.decor(arg=True)
@call_exept(False)
async def callback_handler(callback: CallbackQuery, callback_data: NewItemAdminACtionCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).add.create_after_moderating(callback_data.sketch_id, callback_data.to_create)
    await callback.message.edit_text(msg, reply_markup=markup)




