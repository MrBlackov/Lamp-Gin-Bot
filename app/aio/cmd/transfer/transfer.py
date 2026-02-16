from aiogram import Router
from app.aio.cmd.transfer.newtransfer import new_transfer_router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.transfer import TransferService
from app.aio.cls.callback.transfer import (InfoTransferInfoCall,
                                           InfoTransferBackCall,
                                           InfoTransferPageCall,
                                           InfoTransferStartCall,
                                           InfoTransferStatusCall,
                                           InfoTransferSortedCall,
                                           InfoTransferActionCall,
                                           InfoTransferSearchCall,)
from app.aio.cls.fsm.transfer import InfoTransferState

transfer_router = Router()
transfer_router.include_routers(new_transfer_router)


@new_transfer_router.message(Command('mytransfers'))
@new_transfer_router.message(Command('transfer'), F.text == '/transfer')
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await TransferService(message.from_user.id, state).info.main_menu()
    await message.answer(msg, reply_markup=markup)

@new_transfer_router.callback_query(InfoTransferBackCall.filter(F.where == 'cmd')) 
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferBackCall, state: FSMContext):
    await state.clear()
    msg, markup = await TransferService(callback.from_user.id, state).info.main_menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(InfoTransferBackCall.filter(F.where == 'pages')) 
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferBackCall, state: FSMContext):
    await state.clear()
    msg, markup = await TransferService(callback.from_user.id, state).info.to_pages()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(InfoTransferSortedCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferSortedCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.to_transfer(callback_data.status)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(InfoTransferSearchCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferSearchCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.to_search(callback_data.search_type, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.message(InfoTransferState.search)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await TransferService(message.from_user.id, state).info.search(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

@new_transfer_router.callback_query(InfoTransferInfoCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferInfoCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.transfer(callback_data.transfer_id)
    await callback.message.edit_text(msg, reply_markup=markup)   

@new_transfer_router.callback_query(InfoTransferActionCall.filter(F.to_new_status == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferActionCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.new_status(callback_data.transfer_id, callback_data.new_status)
    await callback.message.edit_text(msg, reply_markup=markup)   

@new_transfer_router.callback_query(InfoTransferActionCall.filter(F.to_complete == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferActionCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.to_complete(callback_data.transfer_id)
    await callback.message.edit_text(msg, reply_markup=markup)  

@new_transfer_router.callback_query(InfoTransferActionCall.filter(F.to_delete == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InfoTransferActionCall, state: FSMContext):
    msg, markup = await TransferService(callback.from_user.id, state).info.to_delete(callback_data.transfer_id)
    await callback.message.edit_text(msg, reply_markup=markup)  
 



@new_transfer_router.message(Command('transfer'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()  
    msg, markup = await TransferService(message.from_user.id, state).info.to_transfer_for_id(command.args)
    await message.answer(msg, reply_markup=markup)

