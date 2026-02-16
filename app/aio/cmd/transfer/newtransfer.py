from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.transfer import TransferService
from app.aio.cls.callback.transfer import (ItemTransferCharIdCall, 
                                           ItemTransferChoiseCharCall, 
                                           ItemTransferStatusEnum, 
                                           ItemTransferTradeStatusCall, 
                                           ItemTransferActionCall, 
                                           ItemTransferStartCall, 
                                           ItemTransferBackCall, 
                                           ItemTransferCharPageCall,
                                           ItemTransferItemIdCall,
                                           ItemTransferItemPageCall,
                                           InfoTransferStartCall)
from app.aio.cls.fsm.transfer import ItemTransferState

new_transfer_router = Router()

@new_transfer_router.message(Command('newtransfer'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await TransferService(message.from_user.id, state).new.new_transfer()
    await message.answer(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'cmd')) 
@new_transfer_router.callback_query(InfoTransferStartCall.filter(F.to_create == True)) 
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferStartCall | InfoTransferStartCall, state: FSMContext):
    await state.clear()
    
    msg, markup = await TransferService(callback.from_user.id, state).new.new_transfer()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'to_trade')) 
@new_transfer_router.callback_query(ItemTransferStartCall.filter(F.to_trade == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferStartCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.new_trade()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_list == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_list_char()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_search == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_search_char(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferCharPageCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferCharPageCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_page_char(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'char_page'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferBackCall, state: FSMContext):
    
    page = await state.get_value('charpage')
    msg, markup = await TransferService(callback.from_user.id, state).new.to_page_char(page)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.message(ItemTransferState.search_char)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await TransferService(message.from_user.id, state).new.search_char(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()


@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'trade_menu')) 
@new_transfer_router.callback_query(ItemTransferCharIdCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferCharIdCall, state: FSMContext):
    
    if type(callback_data) == ItemTransferBackCall:
        char = await state.get_value('char2')
        char_id = char.id
    else:
        char_id = callback_data.char_id
    msg, markup = await TransferService(callback.from_user.id, state).new.trade_menu(char_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_my_char == True))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext):
    await callback.answer("🙂 Это вы", True)
   
@new_transfer_router.callback_query(ItemTransferActionCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferActionCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.add_item(callback_data.action, callback_data.side)
    await callback.message.edit_text(msg, reply_markup=markup)
   
@new_transfer_router.callback_query(ItemTransferItemPageCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferItemPageCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_page_item(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'item_page'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferBackCall, state: FSMContext):
    
    page = await state.get_value('itempage')
    msg, markup = await TransferService(callback.from_user.id, state).new.to_page_item(page)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferItemIdCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferItemIdCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_item_info(callback_data.item_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
        
@new_transfer_router.message(ItemTransferState.item_quantity)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await TransferService(message.from_user.id, state).new.item_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()
    
@new_transfer_router.callback_query(ItemTransferTradeStatusCall.filter(F.status == ItemTransferStatusEnum.CONFIRMED.value))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferTradeStatusCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_send()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferTradeStatusCall.filter(F.status == ItemTransferStatusEnum.CREATED.value))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: ItemTransferTradeStatusCall, state: FSMContext):
    
    msg, markup = await TransferService(callback.from_user.id, state).new.to_created()
    await callback.message.edit_text(msg, reply_markup=markup)

