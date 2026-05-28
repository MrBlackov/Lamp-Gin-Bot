from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.item import ItemService
from app.aio.cmd.item.admin import admin_router
from app.aio.cmd.item.change import change_item_router
from app.aio.cmd.item.newitem import new_item_router
from app.exeption.decorator import exept, call_exept
from app.aio.cls.fsm.item import ListItemSketchsState
from app.aio.cls.callback.item import (ListItemSketchBackCall, 
                                       ListItemSketchToListCall, 
                                       ListItemSketchToPageCall, 
                                       ListItemSketchToQueryCall,
                                       ListItemSketchItemCall,
                                       MenuCall)
from app.aio.cls.fsm.utils import ItemFSM

item_router = Router()
item_router.include_router(admin_router)
item_router.include_router(change_item_router)
item_router.include_router(new_item_router)

@item_router.message(Command('items'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await ItemService(message.from_user.id, state, message).list.get_item_sketchs()
    await message.answer(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchBackCall.filter(F.where == 'cmd'))    
@item_router.callback_query(MenuCall.filter(F.where == 'items'))   
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchToListCall | MenuCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'list').set_state()
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.get_item_sketchs()
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToListCall.filter(F.is_hide == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchToListCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.get_hide_item_sketchs()
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToListCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchToListCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.list_items(back_where='cmd')
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToPageCall.filter()) 
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchToPageCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.list_items(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.callback_query(ListItemSketchToQueryCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchToQueryCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.to_search(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@item_router.message(ListItemSketchsState.name, F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'list')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state, message).list.search(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@item_router.callback_query(ListItemSketchItemCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ListItemSketchItemCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).list.to_item(callback_data.item)
    await callback.message.edit_text(msg, reply_markup=markup)