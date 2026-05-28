from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.cls.callback.char import (
                                       MenuCall,
                                       NewCharBackCall,
                                       NewCharBonusCall,
                                       NewCharGenderCall,
                                       NewCharActionCall,
                                       NewCharNameActionCall,
                                       NewCharNameCall,
                                       NewCharPageNameCall,
                                       NewCharPageSkillCall,
                                       NewCharSkillCall,
                                       )
from app.service.char import Character
from app.exeption.decorator import exept, call_exept
from app.aio.cls.fsm.utils import CharFSM
from app.aio.cls.fsm.char import NewCharState
from app.aio.cls.tips.char import new_char_tips

new_char_router = Router()

@new_char_router.message(Command('newchar'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await Character(message.from_user.id, state, message).new.chouse_gender()
    await message.answer(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharBackCall.filter(F.where == 'gender'))     
@new_char_router.callback_query(MenuCall.filter(F.where == 'newchar'))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.chouse_gender()
    await callback.message.edit_text(msg, reply_markup=markup)
  
@new_char_router.callback_query(NewCharBonusCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharBonusCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.chouse_gender_bonus()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharGenderCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharGenderCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.menu(callback_data.gender)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharBackCall.filter(F.where == 'menu'))  
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharBackCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharActionCall.filter(F.to_skills == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_skills()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharSkillCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharSkillCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.skills(callback_data.skill_tag, callback_data.level, callback_data.is_base)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharBackCall.filter(F.where == 'skills'))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharBackCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_skills()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharActionCall.filter(F.to_add_skills == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_add_skills()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharPageSkillCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharPageSkillCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_page_skills(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_char_router.callback_query(NewCharActionCall.filter(F.to_rename == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_rename(callback_data.name_type)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharBackCall.filter(F.where == 'rename'))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharBackCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_rename()
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharNameActionCall.filter(F.to_random == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharNameActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_random_name(callback_data.name_type)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharNameActionCall.filter(F.to_query == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharNameActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_query_names(callback_data.name_type, callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.message(NewCharState.part_name, F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CharFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await Character(message.from_user.id, state, message).new.query_names(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@new_char_router.callback_query(NewCharPageNameCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharPageNameCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_page_names(callback_data.page)
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharNameActionCall.filter(F.to_delete == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharNameActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.rename(None, 'last')
    await callback.message.edit_text(msg, reply_markup=markup)

@new_char_router.callback_query(NewCharNameCall.filter())     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharNameCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.rename(callback_data.name, callback_data.name_type)
    await callback.message.edit_text(msg, reply_markup=markup)


@new_char_router.callback_query(NewCharActionCall.filter(F.to_description == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.to_description(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)
    
@new_char_router.message(NewCharState.description, F.text.not_contains('/'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = CharFSM(state, 'new')
    msg0 = await fsm.get_value('msg')
    msg, markup = await Character(message.from_user.id, state, message).new.descript(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@new_char_router.callback_query(NewCharActionCall.filter(F.to_create == True))     
@log.decor(arg=True)
@call_exept(tips=new_char_tips, rarity_tips=0.3)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewCharActionCall, state: FSMContext, **kwargs):
    msg, markup = await Character(callback.from_user.id, state, callback.message).new.create(callback_data.is_finished)
    await callback.message.edit_text(msg, reply_markup=markup)
    














