from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.exeption.decorator import exept
from app.aio.cls.callback.char import InventoryItems, InventoryItemsGo

inventory_router = Router()

@inventory_router.message(Command('inventory'))
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg, markup = await Character(message.from_user.id, state).inventory.inventory()
    await message.answer(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGo.filter())     
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
    
