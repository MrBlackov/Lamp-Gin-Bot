from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner, admins
from app.service.item import ItemService
from app.exeption.decorator import exept, call_exept
from app.aio.cls.fsm.item import ChangeItemSketchState
from app.aio.cls.callback.item import (ChangeItemSketchCall,
                                       ChangeItemSketchDeleteItemsCall,
                                       ChangeItemSketchDeleteSketchCall,
                                       ChangeItemSketchBackCall,
                                       ChangeItemSketchItemCall,
                                       ChangeItemSketchToPageCall,
                                       ChangetemSketchItemInCharCall,
                                       ChangeItemSketchIDCall,
                                       ChangeItemSketchAddActionTagCall,
                                       ChangeItemSketchDeleteActionTagCall)
from app.aio.cls.fsm.utils import ItemFSM

change_item_router = Router()

@change_item_router.message(Command('changeitem'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if command.args != None and message.from_user.id in admins:
        msg, markup = await ItemService(message.from_user.id, state, message).change.start(command.args)
        await message.answer(msg, reply_markup=markup)
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')  

@change_item_router.callback_query(ChangeItemSketchIDCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchIDCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.cmd_start(callback_data.sketch_id)
    await callback.message.answer(msg, reply_markup=markup)

@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'info'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchBackCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'change').set_state()
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_sketch()
    await callback.message.edit_text(msg, reply_markup=markup)

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_items == False), ChangeItemSketchCall.filter(F.what == 'action_tag'))     
@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'action')) 
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'change').set_state()
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_change_action_tag()
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.callback_query(ChangeItemSketchAddActionTagCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchAddActionTagCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_add_action_tag(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.message(ChangeItemSketchState.add_action, F.content_type == 'text', F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'change')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state, message).change.add_action_tag(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@change_item_router.callback_query(ChangeItemSketchDeleteActionTagCall.filter(F.is_delete == False))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteActionTagCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_delete_action_tag(callback_data.tag)
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchDeleteActionTagCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteActionTagCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.delete_action_tag(callback_data.tag)
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_nbt == True), ChangeItemSketchCall.filter(F.what == 'nbt'))     
@log.decor(arg=True)
@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'nbt')) 
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'change').set_state()
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.nbt()
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_delete_nbt == True), ChangeItemSketchCall.filter(F.what == 'nbt'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.delete_nbt()
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.what == 'is_hide'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_change_hide()
    await callback.message.edit_text(msg, reply_markup=markup)    

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_items == False))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_change_data(callback_data.what, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)    

@change_item_router.message(ChangeItemSketchState.new_data, F.content_type == 'text', F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'change')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state, message).change.change_data(message.text, message)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()





@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_items == True))   
@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'char_items'))   
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_char_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchToPageCall.filter())     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchToPageCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_page(page=callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchItemCall.filter())     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchItemCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_item(callback_data.item_id)
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'item'))     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchBackCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'change').set_state()
    item_id = await ItemFSM(state, 'change').get_value('item_id')
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_item(item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@change_item_router.callback_query(ChangetemSketchItemInCharCall.filter())     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangetemSketchItemInCharCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_action_inventory(callback.message, callback_data.item_id, callback_data.action)
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.message(ChangeItemSketchState.action_data, F.content_type == 'text', F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'change')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state, message).change.action_inventory(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()



@change_item_router.callback_query(ChangeItemSketchDeleteItemsCall.filter(F.is_delete == False))     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteItemsCall, state: FSMContext, **kwargs):    
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_delete_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchDeleteSketchCall.filter(F.is_delete == False))     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteSketchCall, state: FSMContext, **kwargs):   
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.to_delete_sketch()
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchDeleteItemsCall.filter(F.is_delete == True))     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteItemsCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.delete_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchDeleteSketchCall.filter(F.is_delete == True))     
@log.decor(arg=True)
async def callback_handler(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteSketchCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state, callback.message).change.delete_sketch()
    await callback.message.edit_text(msg, reply_markup=markup) 
    