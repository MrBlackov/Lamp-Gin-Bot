from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import admins
from app.exeption.decorator import exept, call_exept
from app.service.craft import CraftService
from app.aio.cls.callback.craft import (CraftBackCall, 
                                        CraftIdCall, 
                                        CraftPageCall, 
                                        CraftActionCall, 
                                        CraftCreateActionCall,
                                        CraftItemIdCall,
                                        CraftItemPagesCall,
                                        CraftUseCall,
                                        CraftAdminACtionCall,
                                        MenuCall)
from app.aio.cls.fsm.craft import CraftState, AddCraftState
from app.aio.cls.fsm.utils import CraftFSM

craft_router = Router()



@craft_router.message(Command('newcraft'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await CraftService(message.from_user.id, state).add.craft_menu()
    await message.answer(msg, reply_markup=markup)

@craft_router.callback_query(CraftBackCall.filter(F.where == 'craft_menu')) 
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftBackCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.craft_menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftCreateActionCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftCreateActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.add_item(callback_data.action, callback_data.item_type)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftCreateActionCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftCreateActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.add_item(callback_data.action, callback_data.item_type)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftItemPagesCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftItemPagesCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.to_page_item(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftBackCall.filter(F.where == 'item_page'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftBackCall, state: FSMContext, **kwargs):
    page = await CraftFSM(state, 'add').get_value('itempage')
    msg, markup = await CraftService(callback.from_user.id, state).add.to_page_item(page)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftItemIdCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftItemIdCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.to_item_info(callback_data.item_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.message(AddCraftState.item_quantity)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CraftFSM(state, 'add')
    msg0 = await fsm.get_value('msg')
    msg, markup = await CraftService(message.from_user.id, state).add.item_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@craft_router.callback_query(CraftActionCall.filter(F.to_time == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.to_add_time(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftActionCall.filter(F.redact_hide == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.redact_hide(callback_data.hide)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.message(AddCraftState.time)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CraftFSM(state, 'add')
    msg0 = await fsm.get_value('msg')
    msg, markup = await CraftService(message.from_user.id, state).add.add_time(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@craft_router.callback_query(CraftActionCall.filter(F.to_faq == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg = await CraftService(callback.from_user.id, state).add.faq(callback_data.faq)
    await callback.answer(msg, show_alert=True)

@craft_router.callback_query(CraftActionCall.filter(F.to_send == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).add.send_craft(callback_data.tg_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftActionCall.filter(F.to_craft == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback_data.tg_id, state).add.create_craft()
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftAdminACtionCall.filter(F.to_create == True))     
@craft_router.callback_query(CraftAdminACtionCall.filter(F.to_create == False))   
@log.decor(arg=True)
@call_exept(False)
async def callback_handler(callback: CallbackQuery, callback_data: CraftAdminACtionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback_data.tg_id, state).add.accert_new_craft(callback_data.craft_id, callback_data.to_create)
    await callback.message.edit_text(msg, reply_markup=markup)




@craft_router.message(Command('craft'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await CraftService(message.from_user.id, state).info.get_no_hide_craft()
    await message.answer(msg, reply_markup=markup)

@craft_router.callback_query(CraftBackCall.filter(F.where == 'cmd'))  
@craft_router.callback_query(MenuCall.filter(F.where == 'crafts'))       
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).info.get_no_hide_craft()
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftIdCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftIdCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).info.craft(craft_id=callback_data.craft_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftBackCall.filter(F.where == 'craft_info'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftBackCall, state: FSMContext, **kwargs):
    craft_id = await CraftFSM(state).get_value('craft_id')
    msg, markup = await CraftService(callback.from_user.id, state).info.craft(craft_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.callback_query(CraftPageCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftPageCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).info.crafts_page(page=callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)


@craft_router.callback_query(CraftActionCall.filter(F.to_craft_quantity == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftActionCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).info.to_quantity(callback_data.craft_id, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@craft_router.message(CraftState.quantity)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CraftFSM(state)
    msg0 = await fsm.get_value('msg')
    msg, markup = await CraftService(message.from_user.id, state).info.craft_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@craft_router.callback_query(CraftUseCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: CraftUseCall, state: FSMContext, **kwargs):
    msg, markup = await CraftService(callback.from_user.id, state).info.craft_action(callback_data.craft_id, str(callback_data.quantity))
    await callback.message.edit_text(msg, reply_markup=markup)


