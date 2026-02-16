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
                                       AddCharSketch,
                                       AddCharDescript,
                                       AddCharFinish
                                       )
from app.service.char import Character
from app.aio.msg.utils import TextHTML
from app.exeption.decorator import exept, call_exept

add_char_router = Router()

@add_char_router.message(Command('newchar'), F.chat.type == 'private')
@log.decor(arg=True)
@exept
async def cmd_new_char(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    markup = Character(tg_id=user_id).to_create.chouse_gender()
    await message.answer('📲 Выберите пол', reply_markup=markup)

@add_char_router.callback_query(AddCharNameCall.filter(F.back == True))
@log.decor(arg=True)
@exept
async def cmd_new_char(callback: CallbackQuery, callback_data: AddCharNameCall | None = None):
    user_id = callback.from_user.id
    markup = Character(tg_id=user_id).to_create.chouse_gender(callback_data.back if callback_data else False)
    await callback.message.edit_text('📲 Выберите пол', reply_markup=markup)

@add_char_router.message(Command('newchar'), F.chat.type != 'private')
@log.decor(arg=True)
@exept
async def cmd_new_char(message: Message):
    user_id = message.from_user.id
    await message.answer('😕 Создание персонажа происходит в лс')
    
@add_char_router.callback_query(AddCharGenderCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: AddCharGenderCall, state: FSMContext):
    
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_get_sketchs(callback_data.gender, callback_data.to_change)
    await callback.message.edit_text(f'❔ Как выберем имя?', reply_markup=markup)



@add_char_router.callback_query(AddCharRandomNameCall.filter(F.back == True))     
@add_char_router.callback_query(AddCharQueryNameCall.filter(F.back == True))
@log.decor(arg=True)
@call_exept
async def callback_add_char_names(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext):
    
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(callback_data.first_name)
    await callback.message.edit_text(f'Как выберем имя?', reply_markup=markup)
    await state.set_state(CreateCharState.to_create)
    


@add_char_router.callback_query(AddCharNameCall.filter(F.regim == 'query'))
@log.decor(arg=True)        
@call_exept
async def callback_add_char_name_query(callback: CallbackQuery, callback_data: AddCharNameCall, state: FSMContext):
    await callback.answer('Query')
    markup = Character(tg_id=callback.from_user.id).to_create.IKB.query_back(callback_data.first_name)
    await callback.message.edit_text('✒️ Введите', reply_markup=markup)
    await state.update_data(is_first_name=callback_data.first_name, msg=callback.message)
    await state.set_state(CreateCharState.query_value)

@add_char_router.message(CreateCharState.query_value)
@log.decor(arg=True)
@exept
async def msg_query_for_names(message: Message, state: FSMContext):
    msg_text = message.text
    msg = await state.get_value('msg')
    await msg.delete()
    markup, msg_text = await Character(tg_id=message.from_user.id, state=state).to_create.to_query_names_to_pages(None if msg_text == '!all' else msg_text)
    await message.answer(msg_text, reply_markup=markup)
    await message.delete()
    await state.set_state(CreateCharState.to_create)

@add_char_router.callback_query(AddCharQueryNameCall.filter(F.next_page == True))
@log.decor(arg=True)
@call_exept
async def msg_query_for_names(callback: CallbackQuery, callback_data: AddCharQueryNameCall, state: FSMContext):
    await callback.answer('Query')
    print(True)
    markup, msg = await Character(tg_id=callback.message.from_user.id, state=state).to_create.get_name_pages(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)



@add_char_router.callback_query(AddCharNameCall.filter(F.regim == 'random'))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.regeneration == True))
@log.decor(arg=True)      
@call_exept  
async def callback_add_char_name_rnd(callback: CallbackQuery, callback_data: AddCharNameCall | AddCharRandomNameCall, state: FSMContext):
    await callback.answer('Random')
    markup, name = await Character(callback.from_user.id, state).to_create.to_random_name(callback_data.first_name)
    await callback.message.edit_text(f'{name}?', reply_markup=markup)




@add_char_router.callback_query(AddCharQueryNameCall.filter(F.name != None), AddCharQueryNameCall.filter(F.first_name == True))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.name != None), AddCharRandomNameCall.filter(F.first_name == True))
@log.decor(arg=True)     
@call_exept   
async def callback_add_char_name(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext):
    print('IJP')
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(False)
    await state.update_data(first_name = callback_data.name)
    await callback.message.edit_text(f'🎴 Имя: {callback_data.name} \n Как выберем фамилию?', reply_markup=markup)  
  
@add_char_router.callback_query(AddCharSketch.filter(F.back == True))    
@log.decor(arg=True)  
@call_exept      
async def callback_add_char_name(callback: CallbackQuery, callback_data: AddCharSketch, state: FSMContext):
    print('IJP')
    markup = await Character(tg_id=callback.from_user.id, state=state).to_create.to_sketchs(False)
    first_name = await state.get_value('first_name')
    await callback.message.edit_text(f'🎴 Имя: {first_name} \n Как выберем фамилию?', reply_markup=markup)  
    
@add_char_router.callback_query(AddCharNameCall.filter(F.to_pass==True))
@log.decor(arg=True)
@call_exept        
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext):
    first_name = await state.get_value('first_name')
    await state.update_data(lats_name='')
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs()

    await callback.message.edit_text(f'🎴 Имя: {first_name}' '<blockquote>' + text + '</blockquote>', reply_markup=markup)    

@add_char_router.callback_query(AddCharDescript.filter(F.back == True))
@log.decor(arg=True)  
@call_exept      
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharSketch | AddCharDescript, state: FSMContext):
    first_name = await state.get_value('first_name')
    last_name: str = await state.get_value('last_name')
    if first_name and last_name:
        full_name = first_name + ' ' + last_name
    else:
        full_name = first_name
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs(callback_data.id if type(callback_data) == AddCharSketch else 0)

    await callback.message.edit_text(f'🪪 {full_name}' '<blockquote>' + text + '</blockquote>', reply_markup=markup)    

@add_char_router.callback_query(AddCharQueryNameCall.filter(F.name != None), AddCharQueryNameCall.filter(F.first_name == False))
@add_char_router.callback_query(AddCharRandomNameCall.filter(F.name != None), AddCharRandomNameCall.filter(F.first_name == False))
@log.decor(arg=True)       
@call_exept 
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharQueryNameCall | AddCharRandomNameCall, state: FSMContext):
    first_name = await state.get_value('first_name')
    await state.update_data(last_name=callback_data.name)
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs()

    await callback.message.edit_text(f'🪪 {first_name} {callback_data.name} <blockquote>' + text + '</blockquote>', reply_markup=markup)    

@add_char_router.callback_query(AddCharSketch.filter(F.id != None), AddCharSketch.filter(F.another == True))
@log.decor(arg=True)      
@call_exept  
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharSketch, state: FSMContext):
    first_name = await state.get_value('first_name')
    last_name: str = await state.get_value('last_name')
    if first_name and last_name:
        full_name = first_name + ' ' + last_name
    else:
        full_name = first_name
    markup, text = await Character(callback.from_user.id, state).to_create.to_chouse_sketchs(callback_data.id, callback_data.another)
    await callback.message.edit_text(f'🪪 {full_name} <blockquote>' + text + '</blockquote>', reply_markup=markup)    

@add_char_router.callback_query(AddCharSketch.filter(F.id != None), AddCharSketch.filter(F.another == False))
@log.decor(arg=True)     
@call_exept   
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharSketch, state: FSMContext):
    markup, text = await Character(callback.from_user.id, state).to_create.to_descript(callback_data.id)
    await callback.message.edit_text(text, reply_markup=markup)    
    await state.set_state(CreateCharState.description)
    await state.update_data(msg=callback.message)



@add_char_router.callback_query(AddCharDescript.filter(F.to_pass == True), StateFilter(CreateCharState.description))
@log.decor(arg=True)      
@call_exept  
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharSketch, state: FSMContext):
    char = await Character(callback.from_user.id, state).to_create.get_info()
    await callback.message.edit_text(char.info_to_str, reply_markup=await char.markup_to_info())

@add_char_router.message(CreateCharState.description)
@log.decor(arg=True)
@exept
async def msg_query_for_names(message: Message, state: FSMContext):
    if len(message.text) > 1000:
        await message.answer(f'❌ Макс. количесто симловов для описания - 1000, у вас {len(message.text)}') 
        await state.set_state(CreateCharState.description)
        return 
    msg = await state.get_value('msg')
    await msg.delete()
    char = await Character(message.from_user.id, state).to_create.get_info(TextHTML(message.html_text).escape)
    await message.answer(char.info_to_str, reply_markup=await char.markup_to_info())

@add_char_router.callback_query(AddCharFinish.filter(F.go == True))
@log.decor(arg=True)      
@call_exept  
async def callback_add_char_last_name(callback: CallbackQuery, callback_data: AddCharSketch, state: FSMContext):
    to_create = await Character(callback.from_user.id, state).to_create.create()
    if to_create: 
        await callback.message.edit_text('✅ Персонаж создан, просмотреть информацию /mychar')
    else:
        await callback.message.edit_text('❌ Персонаж не создан, ошибка')
    await state.clear()