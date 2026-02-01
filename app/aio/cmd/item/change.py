from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.item import ItemService
from app.exeption.decorator import exept
from app.aio.cls.fsm.item import ChangeItemSketchState
from app.aio.cls.callback.item import (ChangeItemSketchCall,
                                       ChangeItemSketchDeleteItemsCall,
                                       ChangeItemSketchDeleteSketchCall,
                                       ChangeItemSketchBackCall,
                                       ChangeItemSketchItemCall,
                                       ChangeItemSketchToPageCall,
                                       ChangetemSketchItemInCharCall)

change_item_router = Router()

@change_item_router.message(Command('changeitem'))
@log.decor(arg=True)
@exept
async def cmd_add_item_name(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args != None and message.from_user.id == owner:
        msg, markup = await ItemService(message.from_user.id, state).change.start(command.args)
        await message.answer(msg, reply_markup=markup)
    elif message.from_user.id != owner:
        await message.answer('❌ Нет доступа')
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')  

@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'info'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchBackCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_sketch()
    await callback.message.edit_text(msg, reply_markup=markup)

@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_items == False))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_change_data(callback_data.what, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)    

@change_item_router.message(ChangeItemSketchState.new_data)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).change.change_data(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()





@change_item_router.callback_query(ChangeItemSketchCall.filter(F.to_items == True))   
@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'char_items'))   
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_char_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchToPageCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchToPageCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_page(page=callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchItemCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchItemCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_item(callback_data.item_id)
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.callback_query(ChangeItemSketchBackCall.filter(F.where == 'item'))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchBackCall, state: FSMContext):
    await callback.answer()
    item_id = await state.get_value('item_id')
    msg, markup = await ItemService(callback.from_user.id, state).change.to_item(item_id)
    await callback.message.edit_text(msg, reply_markup=markup)

@change_item_router.callback_query(ChangetemSketchItemInCharCall.filter())     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangetemSketchItemInCharCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_action_inventory(callback.message, callback_data.item_id, callback_data.action)
    await callback.message.edit_text(msg, reply_markup=markup) 

@change_item_router.message(ChangeItemSketchState.action_data)
@log.decor(arg=True)
@exept
async def cmd_inventory(message: Message, state: FSMContext):
    msg0 = await state.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).change.action_inventory(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await state.update_data(msg=msg2)
    await state.set_state()
    await msg0.delete()



@change_item_router.callback_query(ChangeItemSketchDeleteItemsCall.filter(F.is_delete == False))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteItemsCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_delete_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchDeleteSketchCall.filter(F.is_delete == False))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteSketchCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.to_delete_sketch()
    await callback.message.edit_text(msg, reply_markup=markup)  

@change_item_router.callback_query(ChangeItemSketchDeleteItemsCall.filter(F.is_delete == True))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteItemsCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.delete_items()
    await callback.message.edit_text(msg, reply_markup=markup)  
    
@change_item_router.callback_query(ChangeItemSketchDeleteSketchCall.filter(F.is_delete == True))     
@log.decor(arg=True)
async def callback_add_char_names(callback: CallbackQuery, callback_data: ChangeItemSketchDeleteSketchCall, state: FSMContext):
    await callback.answer()
    msg, markup = await ItemService(callback.from_user.id, state).change.delete_sketch()
    await callback.message.edit_text(msg, reply_markup=markup) 
    