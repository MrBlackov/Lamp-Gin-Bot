from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.exeption.decorator import exept, call_exept
from app.aio.cls.callback.char import InventoryItems, InventoryItemsGo, InventoryItemsThrow
from app.aio.cls.fsm.char import InventoryState
from app.service.utils import is_natural_int

inventory_router = Router()

@inventory_router.message(Command('inventory'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    await state.clear()
    msg, markup = await Character(message.from_user.id, state).inventory.inventory()
    await message.answer(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGo.filter(F.where == 'inventory'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItems, state: FSMContext):
    
    msg, markup = await Character(callback.from_user.id, state).inventory.inventory()
    await callback.message.edit_text(msg, reply_markup=markup)
    
@inventory_router.callback_query(InventoryItems.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItems, state: FSMContext):
    
    msg, markup = await Character(callback.from_user.id, state).inventory.get_item_info(callback_data.item)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGo.filter(F.where == 'item'))     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItemsGo, state: FSMContext):
    
    item_id = await state.get_value('item')
    msg, markup = await Character(callback.from_user.id, state).inventory.get_item_info(item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsThrow.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItemsThrow, state: FSMContext):
    
    msg, markup = await Character(callback.from_user.id, state).inventory.to_throw(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.message(InventoryState.throw_quantity, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    item_id = await state.get_value('item')
    quan = is_natural_int(message.text, message.from_user.id)
    msg, markup = await Character(message.from_user.id, state).inventory.throw_away(item_id, quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()

