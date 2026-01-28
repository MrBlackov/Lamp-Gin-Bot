from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.item import ItemService
from app.exeption.decorator import exept

faq_router = Router()

@faq_router.message(Command('help'), F.text.contains('error'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Скоро')

@faq_router.message(Command('help'), F.text.contains('char'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Скоро')

@faq_router.message(Command('help'), F.text.contains('item'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Скоро')

@faq_router.message(Command('help'), F.text.contains('cmd'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Скоро')

@faq_router.message(Command('help'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Скоро')