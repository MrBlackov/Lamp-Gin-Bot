from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from datetime import datetime
from app.logged.botlog import log
from aiogram.fsm.context import FSMContext
from app.exeption.decorator import exept

start_router = Router()

@start_router.message(Command('chat_id'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_name = message.from_user.username
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'Topic id: {message.message_thread_id}')       
    await message.delete() 

@start_router.message(Command('cancel'), F.chat.type == 'private')
@log.decor(arg=True)
@exept
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено')
    await message.delete()