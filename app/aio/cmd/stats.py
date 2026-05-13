from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.stats import StatsService
from app.aio.cls.callback.stats import StatsActionCall, StatsBackCall, TopActionCall, TopSkillCall

stats_router = Router()   

@stats_router.message(Command('stats'), F.text == '/stats')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg = await StatsService(message.from_user.id, state).all_coins()
    await message.answer(msg)

@stats_router.callback_query(StatsBackCall.filter(F.where == 'tops'))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: TopActionCall, state: FSMContext, **kwargs):
    msg, markup = await StatsService(callback.from_user.id, state).tops()
    await callback.message.edit_text(msg, reply_markup=markup)

@stats_router.message(Command('tops'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await StatsService(message.from_user.id, state).tops()
    await message.answer(msg, reply_markup=markup)

@stats_router.callback_query(TopActionCall.filter(F.to_skill == True))  
@stats_router.callback_query(StatsBackCall.filter(F.where == 'topskills'))  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: TopActionCall, state: FSMContext, **kwargs):
    msg, markup = await StatsService(callback.from_user.id, state).topskills()
    await callback.message.edit_text(msg, reply_markup=markup)

@stats_router.message(Command('topskills'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = await StatsService(message.from_user.id, state).topskills()
    await message.answer(msg, reply_markup=markup)

@stats_router.callback_query(TopSkillCall.filter())  
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: TopSkillCall, state: FSMContext, **kwargs):
    msg, markup = await StatsService(callback.from_user.id, state).topskill(callback_data.skill_tag)
    await callback.message.edit_text(msg, reply_markup=markup)
