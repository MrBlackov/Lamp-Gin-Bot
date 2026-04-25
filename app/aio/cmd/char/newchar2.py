from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.cls.fsm.char import CreateCharState
from app.aio.cls.callback.char import (
                                       AddCharGenderCall,  
                                       AddCharNameCall, 
                                       AddCharQueryNameCall, 
                                       AddCharRandomNameCall,
                                       AddCharSketchCall,
                                       AddCharDescriptCall,
                                       AddCharFinishCall
                                       )
from app.service.char import Character
from app.aio.msg.utils import TextHTML
from app.exeption.decorator import exept, call_exept
from app.aio.cls.fsm.utils import CharFSM

add_char_router = Router()

@add_char_router.message(Command('newchar2'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await Character(message.from_user.id, state).to_create.chouse_gender()
    await message.answer(msg, reply_markup=markup)

@add_char_router.callback_query(AddCharNameCall.filter(F.get_bonus == True))
@log.decor(arg=True)
@call_exept()
async def cmd_handler(callback: CallbackQuery, callback_data: AddCharNameCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id).to_create.chouse_gender_bonus(callback_data.back if callback_data else False)
    await callback.message.edit_text(msg, reply_markup=markup)

@add_char_router.callback_query(AddCharNameCall.filter(F.back == True))
@log.decor(arg=True)
@call_exept()
async def cmd_handler(callback: CallbackQuery, callback_data: AddCharNameCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id).to_create.chouse_gender(callback_data.back if callback_data else False)
    await callback.message.edit_text(msg, reply_markup=markup)

@add_char_router.callback_query(AddCharGenderCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: AddCharGenderCall, state: FSMContext, **kwargs):
    
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_get_sketchs(callback_data.gender, callback_data.to_change)
    await callback.message.edit_text(f'❔ Как выберем имя?', reply_markup=markup)



@add_char_router.callback_query(AddCharRandomNameCall.filter(F.back == True))     
@add_char_router.callback_query(AddCharQueryNameCall.filter(F.back == True))
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext, **kwargs):
    
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(callback_data.first_name)
    await callback.message.edit_text(f'❔ Как выберем {'имя' if callback_data.first_name else 'фамилию'}?', reply_markup=markup)
    await CharFSM(state, 'add').set_state(CreateCharState.to_create)
    


@add_char_router.callback_query(AddCharNameCall.filter(F.regim == 'query'))
@log.decor(arg=True)        
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: AddCharNameCall, state: FSMContext, **kwargs):
    await callback.answer('Query')
    markup = Character(tg_id=callback.from_user.id).to_create.IKB.query_back(callback_data.first_name)
    await callback.message.edit_text('✒️ Введите', reply_markup=markup)
    await CharFSM(state, 'add').update_data(is_first_name=callback_data.first_name, msg=callback.message)
    await CharFSM(state, 'add').set_state(CreateCharState.query_value)

@add_char_router.message(CreateCharState.query_value)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg_text = message.text
    msg = await CharFSM(state, 'add').get_value('msg')
    await msg.delete()
    markup, msg_text = await Character(tg_id=message.from_user.id, state=state).to_create.to_query_names_to_pages(None if msg_text == '!all' else msg_text)
    await message.answer(msg_text, reply_markup=markup)
    await CharFSM(state, 'add').set_state(CreateCharState.to_create)

@add_char_router.callback_query(AddCharQueryNameCall.filter(F.next_page == True))
@log.decor(arg=True)
@call_exept()
async def cmd_handler(callback: CallbackQuery, callback_data: AddCharQueryNameCall, state: FSMContext, **kwargs):
    await callback.answer('Query')
    print(True)
    markup, msg = await Character(tg_id=callback.message.from_user.id, state=state).to_create.get_name_pages(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)



@add_char_router.callback_query(AddCharNameCall.filter(F.regim == 'random'))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.regeneration == True))
@log.decor(arg=True)      
@call_exept()  
async def callback_handler(callback: CallbackQuery, callback_data: AddCharNameCall | AddCharRandomNameCall, state: FSMContext, **kwargs):
    markup, name = await Character(callback.from_user.id, state).to_create.to_random_name(callback_data.first_name)
    await callback.message.edit_text(f'{name}?', reply_markup=markup)




@add_char_router.callback_query(AddCharQueryNameCall.filter(F.name != None), AddCharQueryNameCall.filter(F.first_name == True))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.name != None), AddCharRandomNameCall.filter(F.first_name == True))
@log.decor(arg=True)     
@call_exept()   
async def callback_handler(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext, **kwargs):
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(False)
    await CharFSM(state, 'add').update_data(first_name = callback_data.name)
    await callback.message.edit_text(f'🎴 Имя: {callback_data.name} \n Как выберем фамилию?', reply_markup=markup)

@add_char_router.callback_query(AddCharSketchCall.filter(F.back == True))
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: AddCharSketchCall, state: FSMContext, **kwargs):
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(False)
    first_name = await CharFSM(state, 'add').get_value('first_name')
    await callback.message.edit_text(f'🎴 Имя: {first_name} \n Как выберем фамилию?', reply_markup=markup)  
    
@add_char_router.callback_query(AddCharNameCall.filter(F.to_pass==True))
@log.decor(arg=True)
@call_exept()        
async def callback_handler(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext, **kwargs):
    first_name = await CharFSM(state, 'add').get_value('first_name')
    await CharFSM(state, 'add').update_data(last_name='')
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs()

    await callback.message.edit_text(f'🎴 Имя: {first_name}' + text, reply_markup=markup)    

@add_char_router.callback_query(AddCharDescriptCall.filter(F.back == True))
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: AddCharSketchCall | AddCharDescriptCall, state: FSMContext, **kwargs):
    first_name = await CharFSM(state, 'add').get_value('first_name')
    last_name: str = await CharFSM(state, 'add').get_value('last_name')
    if first_name and last_name:
        full_name = first_name + ' ' + last_name
    else:
        full_name = first_name
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs(callback_data.id if type(callback_data) == AddCharSketchCall else 0)

    await callback.message.edit_text(f'🪪 {full_name}' + text, reply_markup=markup)    

@add_char_router.callback_query(AddCharQueryNameCall.filter(F.name != None), AddCharQueryNameCall.filter(F.first_name == False))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.name != None), AddCharRandomNameCall.filter(F.first_name == False))
@log.decor(arg=True)       
@call_exept() 
async def callback_handler(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext, **kwargs):
    first_name = await CharFSM(state, 'add').get_value('first_name')
    await CharFSM(state, 'add').update_data(last_name=callback_data.name)
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs()

    await callback.message.edit_text(f'🪪 {first_name} {callback_data.name}' + text, reply_markup=markup)    

@add_char_router.callback_query(AddCharSketchCall.filter(F.id != None), AddCharSketchCall.filter(F.another == True))
@log.decor(arg=True)      
@call_exept()  
async def callback_handler(callback: CallbackQuery, callback_data: AddCharSketchCall, state: FSMContext, **kwargs):
    first_name = await CharFSM(state, 'add').get_value('first_name')
    last_name: str = await CharFSM(state, 'add').get_value('last_name')
    if first_name and last_name:
        full_name = first_name + ' ' + last_name
    else:
        full_name = first_name
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs(callback_data.id, callback_data.another)
    await callback.message.edit_text(f'🪪 {full_name}' + text, reply_markup=markup)    

@add_char_router.callback_query(AddCharSketchCall.filter(F.id != None), AddCharSketchCall.filter(F.another == False))
@log.decor(arg=True)     
@call_exept()   
async def callback_handler(callback: CallbackQuery, callback_data: AddCharSketchCall, state: FSMContext, **kwargs):
    markup, text = await Character(callback.from_user.id, state).to_create.to_descript(callback_data.id)
    await callback.message.edit_text(text, reply_markup=markup)    
    await CharFSM(state, 'add').set_state(CreateCharState.description)
    await CharFSM(state, 'add').update_data(msg=callback.message)



@add_char_router.callback_query(AddCharDescriptCall.filter(F.to_pass == True), StateFilter(CreateCharState.description))
@log.decor(arg=True)      
@call_exept()  
async def callback_handler(callback: CallbackQuery, callback_data: AddCharDescriptCall, state: FSMContext, **kwargs):
    char = await Character(callback.from_user.id, state).to_create.get_info()
    await callback.message.edit_text(char.info_to_str, reply_markup=await char.markup_to_info())

@add_char_router.message(CreateCharState.description)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    if len(message.text) > 1000:
        await message.answer(f'❌ Макс. количесто симловов для описания - 1000, у вас {len(message.text)}') 
        await CharFSM(state, 'add').set_state(CreateCharState.description)
        return 
    msg = await CharFSM(state, 'add').get_value('msg')
    await msg.delete()
    char = await Character(message.from_user.id, state).to_create.get_info(TextHTML(message.html_text).escape)
    await message.answer(char.info_to_str, reply_markup=await char.markup_to_info())

@add_char_router.callback_query(AddCharFinishCall.filter(F.go == True))
@log.decor(arg=True)      
@call_exept()  
async def callback_handler(callback: CallbackQuery, callback_data: AddCharFinishCall, state: FSMContext, **kwargs):
    to_create = await Character(callback.from_user.id, state).to_create.create()
    if to_create: 
        await callback.message.edit_text('✅ Персонаж создан, просмотреть информацию /mychar')
    else:
        await callback.message.edit_text('❌ Персонаж не создан, ошибка')