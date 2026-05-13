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
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner, bot
from app.service.main import UserService
from app.exeption.decorator import exept
from aiogram.methods import CreateForumTopic
from app.aio.middlewares.message_clean import MessageCleanDpMiddleware

base_router = Router()
base_router.include_routers(setting_router, char_router, action_router, social_router, skill_router, faq_router, chat_router, stats_router)
base_router.message.middleware(MessageCleanDpMiddleware())

@base_router.message(Command('menu'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    msg, markup = UserService(message.from_user.id, state).menu()
    await message.answer(msg, reply_markup=markup)

@base_router.message(Command('user'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if command.args != None and message.from_user.id == owner:
        msg = await UserService(message.from_user.id, state).get_info(command.args)
        await message.answer(msg)
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')

@base_router.message(Command('topic'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    topic = await bot(CreateForumTopic(chat_id=message.from_user.id, name='Test', icon_color=7322096))
    await bot.send_message(message.chat.id, f'Готово, id: {topic.message_thread_id}', message_thread_id=topic.message_thread_id)
        

@base_router.message(Command('chat_id'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message, **kwargs):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_name = message.from_user.username
    await message.answer(f'Chat id: {message.chat.id}')
    if message.is_topic_message:
        await message.answer(f'Topic id: {message.message_thread_id}')    

@base_router.message(Command('cancel'))
@log.decor(arg=True)
@exept
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    await state.set_state()
    await message.answer('Отмена произошла успешно')

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