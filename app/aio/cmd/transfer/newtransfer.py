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
from app.aio.cls.fsm.utils import TransferFSM

new_transfer_router = Router()

@new_transfer_router.message(Command('newtransfer'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await TransferService(message.from_user.id, state, message).new.new_transfer()
    await message.answer(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'cmd')) 
@new_transfer_router.callback_query(InfoTransferStartCall.filter(F.to_create == True)) 
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferStartCall | InfoTransferStartCall, state: FSMContext, **kwargs):
    
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.new_transfer()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'to_trade')) 
@new_transfer_router.callback_query(ItemTransferStartCall.filter(F.to_trade == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferStartCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.new_trade()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_list == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_list_char()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_search == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_search_char(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferCharPageCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferCharPageCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_page_char(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'char_page'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferBackCall, state: FSMContext, **kwargs):
    page = await TransferFSM(state, 'new').get_value('charpage')
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_page_char(page)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.message(ItemTransferState.search_char, F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = TransferFSM(state, 'new')   
    msg0 = await fsm.get_value('msg')
    msg, markup = await TransferService(message.from_user.id, state, message).new.search_char(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()


@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'trade_menu')) 
@new_transfer_router.callback_query(ItemTransferCharIdCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferCharIdCall, state: FSMContext, **kwargs):
    if type(callback_data) == ItemTransferBackCall:
        char = await TransferFSM(state, 'new').get_value('char2')
        char_id = char.id
    else:
        char_id = callback_data.char_id
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.trade_menu(char_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferChoiseCharCall.filter(F.to_my_char == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferChoiseCharCall, state: FSMContext, **kwargs):
    await callback.answer("🙂 Это вы", True)
   
@new_transfer_router.callback_query(ItemTransferActionCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferActionCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.add_item(callback_data.action, callback_data.side)
    await callback.message.edit_text(msg, reply_markup=markup)
   
@new_transfer_router.callback_query(ItemTransferItemPageCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferItemPageCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_page_item(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferBackCall.filter(F.where == 'item_page'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferBackCall, state: FSMContext, **kwargs):
    page = await TransferFSM(state, 'new').get_value('itempage')
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_page_item(page)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_transfer_router.callback_query(ItemTransferItemIdCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferItemIdCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_item_info(callback_data.item_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
        
@new_transfer_router.message(ItemTransferState.item_quantity, F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = TransferFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await TransferService(message.from_user.id, state, message).new.item_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()
    
@new_transfer_router.callback_query(ItemTransferTradeStatusCall.filter(F.status == ItemTransferStatusEnum.CONFIRMED.value))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferTradeStatusCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_send()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_transfer_router.callback_query(ItemTransferTradeStatusCall.filter(F.status == ItemTransferStatusEnum.CREATED.value))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ItemTransferTradeStatusCall, state: FSMContext, **kwargs):
    msg, markup = await TransferService(callback.from_user.id, state, callback.message).new.to_created()
    await callback.message.edit_text(msg, reply_markup=markup)

