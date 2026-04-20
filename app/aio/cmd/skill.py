from aiogram import Router
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.exeption.decorator import exept, call_exept
from app.service.skill import SkillService, SkillFSM
from app.aio.cls.callback.skill import SkillBack

skill_router = Router()

@skill_router.message(Command('myskill'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    msg, markup = await SkillService(message.from_user.id, state)
    await message.answer(msg, reply_markup=markup)

@skill_router.callback_query(SkillBack.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: SkillBack, state: FSMContext, **kwargs):
    msg, markup = SkillService(callback.from_user.id, state)
    await callback.message.answer(msg, reply_markup=markup)


