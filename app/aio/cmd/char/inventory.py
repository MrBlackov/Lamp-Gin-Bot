from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.exeption.decorator import exept
from app.aio.cls.callback.char import InventoryItems, InventoryItemsGo, InventoryItemsThrow
from app.aio.cls.fsm.char import InventoryState
from app.exeption.item import ThrowAwayQuantityNoInt

inventory_router = Router()

@inventory_router.message(Command('inventory'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg, markup = await Character(message.from_user.id, state).inventory.inventory()
    await message.answer(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGo.filter(F.where == 'inventory'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItems, state: FSMContext):
    await callback.answer()
    msg, markup = await Character(callback.from_user.id, state).inventory.inventory()
    await callback.message.answer(msg, reply_markup=markup)
    
@inventory_router.callback_query(InventoryItems.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItems, state: FSMContext):
    await callback.answer()
    msg, markup = await Character(callback.from_user.id, state).inventory.get_item_info(callback_data.item)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGo.filter(F.where == 'item'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItemsGo, state: FSMContext):
    await callback.answer()
    item_id = await state.get_value('item')
    msg, markup = await Character(callback.from_user.id, state).inventory.get_item_info(item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsThrow.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: InventoryItemsThrow, state: FSMContext):
    await callback.answer()
    msg, markup = await Character(callback.from_user.id, state).inventory.to_throw()
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.message(InventoryState.throw_quantity, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    item_id = await state.get_value('item')
    if message.text.isalnum() == False:
        raise ThrowAwayQuantityNoInt(f'This user({message.fron_user.id}) enter no int')
    msg, markup = await Character(message.from_user.id, state).inventory.throw_away(item_id, int(message.text))
    await message.answer(msg, reply_markup=markup)

