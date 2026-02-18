from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.aio.cmd.char.newchar import add_char_router
from app.aio.cmd.item.items import item_router
from app.aio.cmd.char.inventory import inventory_router
from app.aio.cls.callback.char import (
                                       InfoCharChouse, 
                                       InfoCharList,
                                       CallbackData
                                       )
from app.exeption.decorator import exept, call_exept

char_router = Router()
char_router.include_router(add_char_router)
char_router.include_router(item_router)
char_router.include_router(inventory_router)

@char_router.message(Command('mychar'))
@log.decor(arg=True)
@exept
async def cmd_new_char(message: Message, state: FSMContext):
    await state.clear()
    markup, text = await Character(message.from_user.id, state).info.get_chars()
    await message.answer(text, reply_markup=markup)
    
@add_char_router.callback_query(InfoCharChouse.filter(F.back == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoCharChouse, state: FSMContext):
    
    markup, text = await Character(callback.from_user.id, state).info.get_chars()
    await callback.message.edit_text(text, reply_markup=markup)

@add_char_router.callback_query(InfoCharList.filter())         
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoCharList, state: FSMContext):
    
    markup, text = await Character(callback.from_user.id, state).info.get_char(callback_data.char_id)
    await callback.message.edit_text(text, reply_markup=markup)

@add_char_router.callback_query(InfoCharChouse.filter())         
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoCharList, state: FSMContext):
    
    markup, text = await Character(callback.from_user.id, state).info.char_to_main(callback_data.char_id)
    await callback.message.edit_text(text, reply_markup=markup)    






