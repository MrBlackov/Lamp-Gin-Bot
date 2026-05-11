from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.aio.cmd.char.newchar import new_char_router
from app.aio.cmd.item.items import item_router
from app.aio.cmd.item.craft import craft_router
from app.aio.cmd.char.inventory import inventory_router
from app.aio.cmd.transfer.transfer import transfer_router
from app.aio.cmd.transfer.transfer import transfer_router
from app.aio.cls.callback.char import (
                                       InfoCharChooseCall, 
                                       InfoCharListCall,
                                       InfoCharDeleteCall,
                                       MenuCall
                                       )
from app.exeption.decorator import exept, call_exept

char_router = Router()
char_router.include_routers(new_char_router, item_router, inventory_router, transfer_router, craft_router)

@char_router.message(Command('mychar'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    markup, text = await Character(message.from_user.id, state).info.get_main_char()
    await message.answer(text, reply_markup=markup)

@char_router.callback_query(MenuCall.filter(F.where == 'mychar'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: MenuCall, state: FSMContext, **kwargs):
    markup, msg = await Character(callback.from_user.id, state).info.get_main_char()
    await callback.message.edit_text(msg, reply_markup=markup)

@char_router.message(Command('mychars'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    markup, text = await Character(message.from_user.id, state).info.get_chars()
    await message.answer(text, reply_markup=markup)
    
@char_router.callback_query(MenuCall.filter(F.where == 'mychars'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: MenuCall, state: FSMContext, **kwargs):
    markup, msg = await Character(callback.from_user.id, state).info.get_chars()
    await callback.message.edit_text(msg, reply_markup=markup)

@char_router.callback_query(InfoCharChooseCall.filter(F.back == True))   
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InfoCharChooseCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).info.get_chars()
    await callback.message.edit_text(text, reply_markup=markup)

@char_router.callback_query(InfoCharListCall.filter()) 
@char_router.callback_query(InfoCharDeleteCall.filter(F.back == True))           
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InfoCharListCall | InfoCharDeleteCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).info.get_char(callback_data.char_id)
    await callback.message.edit_text(text, reply_markup=markup)

@char_router.callback_query(InfoCharChooseCall.filter())         
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InfoCharChooseCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).info.char_to_main(callback_data.char_id)
    await callback.message.edit_text(text, reply_markup=markup)    

@char_router.callback_query(InfoCharDeleteCall.filter(F.is_delete == False))         
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InfoCharDeleteCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).info.to_delete_char(callback_data.char_id, callback_data.exist_id)
    await callback.message.edit_text(text, reply_markup=markup)   

@char_router.callback_query(InfoCharDeleteCall.filter(F.is_delete == True))         
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InfoCharDeleteCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).info.delete_char(callback_data.exist_id)
    await callback.message.edit_text(text, reply_markup=markup)   




