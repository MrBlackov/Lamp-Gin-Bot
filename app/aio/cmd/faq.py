from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.faq import FaqService
from app.exeption.decorator import exept, call_exept
from app.exeption.faq import FaqErrorNoEnterError, FaqErrorNoFindError
from app.aio.cls.callback.faq import ToErrorFAQCall
from app.aio.cls.callback.item import NewItemACtionCall

faq_router = Router()   

@faq_router.callback_query(ToErrorFAQCall.filter())     
@log.decor(arg=True)
@call_exept
async def callback_to_error_faq(callback: CallbackQuery, callback_data: ToErrorFAQCall, state: FSMContext):
    msg, markup = FaqService(callback.from_user.id, state).to_error_faq(callback.message.text, callback_data.code)
    await callback.message.edit_text(msg, reply_markup=markup)

@faq_router.callback_query(NewItemACtionCall.filter(F.to_read_rules == True))     
@log.decor(arg=True)
@call_exept
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = FaqService(callback.from_user.id, state).to_item_rules()
    await callback.message.answer(msg, reply_markup=markup)


@faq_router.message(Command('help'), F.text.contains('error'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, command: CommandObject, state: FSMContext):
    code = command.args.replace('error ', '')
    print(command.args)
    if code == None:
        raise FaqErrorNoEnterError(f'This user(tg_id:{message.from_user.id}) dont enter code for error')
    msg, markup = FaqService(message.from_user.id, state).help_error_faq(code)
    await message.answer(msg, reply_markup=markup)

@faq_router.message(Command('faqerror'))
@faq_router.message(Command('helperror'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, command: CommandObject, state: FSMContext):
    code = command.args
    if code == None:
        raise FaqErrorNoEnterError(f'This user(tg_id:{message.from_user.id}) dont enter code for error')
    msg, markup = FaqService(message.from_user.id, state).help_error_faq(code)
    await message.answer(msg, reply_markup=markup)

    

@faq_router.message(Command('help'), F.text.contains('char'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    msg, markup = FaqService(message.from_user.id, state).help_chars()
    await message.answer(msg, reply_markup=markup)

@faq_router.message(Command('help'), F.text.contains('item'))
@faq_router.message(Command('helpitem'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    msg, markup = FaqService(message.from_user.id, state).help_items()
    await message.answer(msg, reply_markup=markup)

@faq_router.callback_query(NewItemACtionCall.filter(F.to_faq == True))     
@log.decor(arg=True)
@call_exept
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: NewItemACtionCall, state: FSMContext):
    msg, markup = FaqService(callback.from_user.id, state).help_items()
    await callback.message.answer(msg, reply_markup=markup)

@faq_router.message(Command('helpcmd'))
@faq_router.message(Command('help'), F.text.contains('cmd'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    msg, markup = FaqService(message.from_user.id, state).help_cmd()
    await message.answer(msg, reply_markup=markup)

@faq_router.message(Command('help'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    msg, markup = FaqService(message.from_user.id, state).help()
    await message.answer(msg, reply_markup=markup)

@faq_router.message(Command('start'))
@log.decor(arg=True)
@exept
async def cmd_help(message: Message, state: FSMContext):
    msg, markup = FaqService(message.from_user.id, state).to_start(message.from_user.full_name)
    await message.answer(msg, reply_markup=markup)