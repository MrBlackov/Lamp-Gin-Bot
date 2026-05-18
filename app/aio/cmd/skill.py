from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.skill import SkillService, SkillFSM
from app.aio.cls.callback.skill import SkillBackCall, SkillCall, SkillPageCall, MenuCall

skill_router = Router()

@skill_router.message(Command('myskills'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await SkillService(message.from_user.id, state, message).get_my_skills()
    await message.answer(msg, reply_markup=markup)

@skill_router.callback_query(SkillBackCall.filter(F.where == 'myskills'))     
@skill_router.callback_query(MenuCall.filter(F.where == 'myskills'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SkillBackCall | MenuCall, state: FSMContext, **kwargs):
    msg, markup = await SkillService(callback.from_user.id, state, callback.message).get_my_skills()
    await callback.message.edit_text(msg, reply_markup=markup)
    
@skill_router.callback_query(SkillCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SkillCall, state: FSMContext, **kwargs):
    msg, markup = await SkillService(callback.from_user.id, state, callback.message).skill(callback_data.skill_id)
    await callback.message.edit_text(msg, reply_markup=markup)
