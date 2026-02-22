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
                                       NewItemAdminACtionCall)

new_item_router = Router()


@new_item_router.message(Command('newitem'), F.text.contains('y'))
@new_item_router.message(Command('newitem'), F.text.contains('yes'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await ItemService(message.from_user.id, state).add.to_name()
    msg0 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg0)

@new_item_router.message(Command('newitem'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await ItemService(message.from_user.id, state).add.to_create_item()
    await message.answer(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_argree_rules == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_name()
    await callback.message.edit_text(msg, reply_markup=markup)
    await state.update_data(msg=callback.message)

@new_item_router.message(NewItemState.to_name)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.to_emodzi(message.text, message)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await msg0.delete()

@new_item_router.message(NewItemState.to_emodzi)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.to_menu(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

@new_item_router.callback_query(NewItemBackCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemBackCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_redact == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_redact(callback_data.redact_key, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.message(NewItemState.to_redact)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).add.redact(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_send == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.to_send()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemACtionCall.filter(F.to_create == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.create()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_create == True))     
@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_create == False))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemAdminACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.create_after_moderating(callback_data.sketch_id, callback_data.to_create)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_item_router.callback_query(NewItemAdminACtionCall.filter(F.to_redact == False))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: NewItemAdminACtionCall, state: FSMContext):
    msg, markup = await ItemService(callback.from_user.id, state).add.create_after_moderating(callback_data.sketch_id, callback_data.to_create)
    await callback.message.edit_text(msg, reply_markup=markup)




