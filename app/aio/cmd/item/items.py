from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.item import ItemService
from app.aio.cmd.item.add_and_give import add_item_router
from app.aio.cmd.item.change import change_item_router
from app.exeption.decorator import exept
from app.aio.cls.fsm.item import ListItemSketchsState
from app.aio.cls.callback.item import (ListItemSketchBackCall, 
                                       ListItemSketchToListCall, 
                                       ListItemSketchToPageCall, 
                                       ListItemSketchToQueryCall,
                                       ListItemSketchItemCall)

item_router = Router()
item_router.include_router(add_item_router)
item_router.include_router(change_item_router)

@item_router.message(Command('items'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await ItemService(message.from_user.id, state).list.get_item_sketchs()
    await message.answer(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchBackCall.filter(F.where == 'cmd'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ListItemSketchToListCall, state: FSMContext):
    await callback.answer("⌛")
    msg, markup = await ItemService(callback.from_user.id, state).list.get_item_sketchs()
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToListCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ListItemSketchToListCall, state: FSMContext):
    await callback.answer("⌛")
    msg, markup = await ItemService(callback.from_user.id, state).list.list_items(back_where='cmd')
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToPageCall.filter()) 
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ListItemSketchToPageCall, state: FSMContext):
    await callback.answer("⌛")
    msg, markup = await ItemService(callback.from_user.id, state).list.list_items(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToQueryCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ListItemSketchToQueryCall, state: FSMContext):
    await callback.answer("⌛")
    msg, markup = await ItemService(callback.from_user.id, state).list.to_search(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.message(ListItemSketchsState.name)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).list.search(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

@item_router.callback_query(ListItemSketchItemCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ListItemSketchItemCall, state: FSMContext):
    await callback.answer("⌛")
    msg, markup = await ItemService(callback.from_user.id, state).list.to_item(callback_data.item)
    await callback.message.edit_text(msg, reply_markup=markup)