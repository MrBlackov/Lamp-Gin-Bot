from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.service.char import Character
from app.exeption.decorator import exept, call_exept
from app.aio.cls.callback.char import InventoryItemsCall, InventoryItemsGoCall, InventoryItemsActionCall, InventoryItemsPickUpCall, MenuCall
from app.aio.cls.fsm.char import InventoryState
from app.service.utils import is_natural_int
from app.aio.cls.fsm.utils import CharFSM
from app.exeption.item import PickUpQuantityFloat, PickUpQuantityLessOne, PickUpQuantityNoInt
from app.scheduler.message import MessageUtils

inventory_router = Router()

@inventory_router.message(Command('inventory')) 
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await Character(message.from_user.id, state, message).inventory.inventory()
    await message.answer(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGoCall.filter(F.where == 'inventory'))     
@inventory_router.callback_query(MenuCall.filter(F.where == 'inventory'))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.inventory()
    await callback.message.edit_text(msg, reply_markup=markup)
    
@inventory_router.callback_query(InventoryItemsCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.get_item_info(callback_data.item)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGoCall.filter(F.where == 'item'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsGoCall, state: FSMContext, **kwargs):
    item_id = await CharFSM(state, 'inventory').get_value('item') or callback_data.item_id
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.get_item_info(item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsActionCall.filter(F.to_throw == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.to_throw(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.message(InventoryState.throw_quantity, F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CharFSM(state, 'inventory')
    msg0 = await fsm.get_value('msg')
    item_id = await fsm.get_value('item')
    quan = is_natural_int(message.text, message.from_user.id)
    msg, markup = await Character(message.from_user.id, state, message).inventory.throw_away(item_id, quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()



@inventory_router.message(Command('lookaround')) 
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await Character(message.from_user.id, state, message).inventory.cmd_pick_up()
    await message.answer(msg, reply_markup=markup)
                         
@inventory_router.callback_query(InventoryItemsActionCall.filter(F.to_pick_up == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsGoCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.cmd_pick_up()
    await callback.message.edit_text(msg, reply_markup=markup) 

@inventory_router.callback_query(InventoryItemsGoCall.filter(F.where == 'location_items'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsGoCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.cmd_pick_up(callback_data.item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsGoCall.filter(F.where == 'location_item'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsGoCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.look_location_item(callback_data.item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsPickUpCall.filter(F.to_pick_up == False))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsPickUpCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.look_location_item(callback_data.item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.callback_query(InventoryItemsPickUpCall.filter(F.to_pick_up == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: InventoryItemsPickUpCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).inventory.to_pick_up(callback_data.item_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@inventory_router.message(InventoryState.pick_up_quantity)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CharFSM(state, 'inventory')
    msg0 = await fsm.get_value('msg')
    quan = is_natural_int(message.text, 
                          message.from_user.id,
                          PickUpQuantityLessOne,
                          PickUpQuantityFloat,
                          PickUpQuantityNoInt)
    msg, markup = await Character(message.from_user.id, state, message).inventory.pick_up(quan)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()


