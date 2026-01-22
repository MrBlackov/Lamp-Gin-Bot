from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.aio.cls.fsm.item import AddItemState
from app.aio.cls.callback.item import AddItemBackCall, AddItemTypeCall, AddItemMisskCall, AddItemToCreate
from app.exeption.service import ValidToTypeError
from app.service.item import ItemService

add_item_router = Router()

@add_item_router.message(Command('newitem'), F.contente_type == 'document')
@log.decor(arg=True)
async def cmd_add_item_name(message: Message, state: FSMContext):
    await ItemService(message.from_user.id, state).newitem(document=message.document)

@add_item_router.message(Command('newitem'))
@log.decor(arg=True)
async def cmd_add_item_name(message: Message, state: FSMContext):
    await ItemService(message.from_user.id, state).newitem(string=message.text)







@add_item_router.callback_query(AddItemBackCall.filter(F.where == 'name'))
@log.decor(arg=True)
async def callback_add_item(callback: CallbackQuery, callback_data: AddItemBackCall, state: FSMContext):
    text = await Character(callback.from_user.id, state).item.to_name()
    msg = await callback.message.edit_text(text)
    await state.update_data(msg=[msg])

@add_item_router.message(AddItemState.name)
@log.decor(arg=True)
async def cmd_add_item_type(message: Message, state: FSMContext):
    msg_list = []
    try:
        text, markup = await Character(message.from_user.id, state).item.to_type(message.text)
        msg = await message.answer(text, reply_markup=markup)
        msg_list = [msg]
    except ValidToTypeError as e:
        msg2 = await message.answer(e.msg)
        text = await Character(message.from_user.id, state).item.to_name()
        msg = await message.answer(text)
        msg_list =[msg, msg2]
    finally:
        msgs = await state.get_value('msg')
        [await msg_.delete() for msg_ in msgs]
        await state.update_data(msg=msg_list) 

@add_item_router.callback_query(AddItemTypeCall.filter())
@log.decor(arg=True)
async def callback_add_item(callback: CallbackQuery, callback_data: AddItemTypeCall, state: FSMContext):
        text, markup = await Character(callback.from_user.id, state).item.to_default_quantity(callback_data.type)
        msg = await callback.message.edit_text(text, reply_markup=markup)
        await state.update_data(msg=[msg])

@add_item_router.message(AddItemState.quantity)
@log.decor(arg=True)
async def cmd_add_item(message: Message, state: FSMContext):
    msg_list = []
    try:
        text, markup = await Character(message.from_user.id, state).item.to_description(message.text)
        msg = await message.answer(text, reply_markup=markup)
        msg_list = [msg]
    except ValidToTypeError as e:
        msg2 = await message.answer(e.msg)
        text, markup = await Character(message.from_user.id, state).item.to_default_quantity(is_error=True)
        msg = await message.answer(text, reply_markup=markup)
        msg_list =[msg, msg2]
    finally:
        msgs = await state.get_value('msg')
        [await msg_.delete() for msg_ in msgs]
        await state.update_data(msg=msg_list)   
    
@add_item_router.callback_query(AddItemMisskCall.filter(F.where == 'description'))
@log.decor(arg=True)
async def callback_add_item(callback: CallbackQuery, callback_data: AddItemMisskCall, state: FSMContext):
        text, markup = await Character(callback.from_user.id, state).item.to_description()
        msg = await callback.message.edit_text(text, reply_markup=markup)
        await state.update_data(msg=[msg])

@add_item_router.message(AddItemState.description)
@log.decor(arg=True)
async def cmd_add_item(message: Message, state: FSMContext):
    msg_list = []
    try:
        text, markup = await Character(message.from_user.id, state).item.to_check_create(message.text)
        msg = await message.answer(text, reply_markup=markup)
        msg_list = [msg]
    except ValidToTypeError as e:
        msg2 = await message.answer(e.msg)
        text, markup = await Character(message.from_user.id, state).item.to_description(is_error=True)
        msg = await message.answer(text, reply_markup=markup)
        msg_list =[msg, msg2]
    finally:
        msgs = await state.get_value('msg')
        [await msg_.delete() for msg_ in msgs]
        await state.update_data(msg=msg_list)   
    
@add_item_router.callback_query(AddItemMisskCall.filter(F.where == 'to_create'))
@log.decor(arg=True)
async def callback_add_item(callback: CallbackQuery, callback_data: AddItemMisskCall, state: FSMContext):
        text, markup = await Character(callback.from_user.id, state).item.to_check_create()
        msg = await callback.message.edit_text(text, reply_markup=markup)
        await state.update_data(msg=[msg])

@add_item_router.callback_query(AddItemToCreate.filter(F.to_create == True))
@log.decor(arg=True)
async def callback_add_item(callback: CallbackQuery, callback_data: AddItemMisskCall, state: FSMContext):
    text = await Character(callback.from_user.id, state).item.to_create()
    msg = await callback.message.edit_text(text)
    await state.clear()
