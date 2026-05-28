from aiogram import Router, F
from app.aio.cmd.char.mychar import char_router
from app.aio.cmd.faq import faq_router
from app.aio.cmd.kit.kit import kit_router
from app.aio.cmd.stats import stats_router
from app.aio.cmd.setting import setting_router
from app.aio.cmd.social import social_router
from app.aio.cmd.skill import skill_router
from app.aio.cmd.action.action import action_router
from app.aio.cmd.main.chat import chat_router
from app.aio.cmd.drop import drop_router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner, bot, admins
from app.service.main import UserService
from app.exeption.decorator import exept, call_exept
from aiogram.methods import CreateForumTopic
from app.aio.middlewares.message_clean import MessageCleanDpMiddleware
from app.aio.cls.callback.base import MenuCall
from app.aio.msg.utils import TextHTML

base_router = Router()
base_router.include_routers(setting_router, char_router, action_router, social_router, skill_router, faq_router, chat_router, drop_router, stats_router)
base_router.message.middleware(MessageCleanDpMiddleware())

@base_router.message(Command('menu'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = UserService(message.from_user.id, state, message).menu()
    await message.answer(msg, reply_markup=markup)


@faq_router.callback_query(MenuCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept()
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: MenuCall, state: FSMContext, **kwargs):
    msg, markup = UserService(callback.from_user.id, state, callback.message).menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@base_router.message(Command('user'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if command.args != None and message.from_user.id in admins:
        msg = await UserService(message.from_user.id, state, message).get_info(command.args)
        await message.answer(msg)
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')

@base_router.message(Command('getlogs'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if message.from_user.id == owner:
        msg, reply_markup = await UserService(message.from_user.id, state, message).get_logs()
        await message.answer(msg, reply_markup=reply_markup)

@base_router.message(Command('topic'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    topic = await bot(CreateForumTopic(chat_id=message.from_user.id, name='Test', icon_color=7322096))
    await bot.send_message(message.chat.id, f'Готово, id: {topic.message_thread_id}', message_thread_id=topic.message_thread_id)
        

@base_router.message(Command('chat_id'))
@base_router.message(Command('topic_id'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message, **kwargs):
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'\nTopic id: {message.message_thread_id}')    

@base_router.message(Command('cancel'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    await state.set_state()
    await message.answer('✅ Отмена произошла успешно')

@faq_router.callback_query(MenuCall.filter(F.where == 'cancel'))     
@log.decor(arg=True)
async def callback_to_new_item_faq(callback: CallbackQuery, callback_data: MenuCall, state: FSMContext, **kwargs):
    await state.set_state()
    await callback.message.edit_text('✅ Отмена произошла успешно')

@base_router.message(Command('emodzi'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                custom_emoji_id = entity.custom_emoji_id
                await message.answer(f"ID эмодзи: {custom_emoji_id}, эмодзи <tg-emoji emoji-id='{custom_emoji_id}'>🤔</tg-emoji>")
                break