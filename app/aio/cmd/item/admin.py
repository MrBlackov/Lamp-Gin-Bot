from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from app.logged.botlog import log
from app.aio.config import owner
from app.service.item import ItemService, ItemFSM
from app.exeption.decorator import exept, call_exept
from app.aio.cls.callback.item import GiveItemCall, GiveItemActionCall, GiveItemBackCall
from app.aio.cls.fsm.item import GiveItemState

admin_router = Router()

@admin_router.message(Command('additem'), F.content_type == 'text')
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if command.args != None and message.from_user.id == owner:
        msg = await ItemService(message.from_user.id).add.add_data_item(command.args)
        await message.answer(msg)
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')

@admin_router.message(Command('giveitem'))
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, command: CommandObject, state: FSMContext, **kwargs):
    if command.args != None and message.from_user.id == owner:
        msg = await ItemService(message.from_user.id).give.give(command.args)
        await message.answer(msg)
    elif command.args == None:
        await message.answer('⁉️ Где данные?')
    else:
        await message.answer('⁉️ Неизввестная ошибка')
     
@admin_router.callback_query(GiveItemCall.filter())     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: GiveItemCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).give.to_give_menu(callback_data.sketch_id)
    await callback.message.answer(msg, reply_markup=markup)

@admin_router.callback_query(GiveItemBackCall.filter(F.where == 'menu'))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: GiveItemCall, state: FSMContext, **kwargs):
    await ItemFSM(state, 'give').set_state()
    msg, markup = await ItemService(callback.from_user.id, state).give.give_menu()
    await callback.message.edit_text(msg, reply_markup=markup)

@admin_router.callback_query(GiveItemActionCall.filter(F.to_quantity == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: GiveItemCall, state: FSMContext, **kwargs):
    msg, markup = await ItemService(callback.from_user.id, state).give.to_change_quantity(callback.message)
    await callback.message.edit_text(msg, reply_markup=markup)

@admin_router.message(GiveItemState.change_quantity)
@log.decor(arg=True)
@exept
async def cmd_handler(message: Message, state: FSMContext, **kwargs):
    fsm = ItemFSM(state, 'give')
    msg0 = await fsm.get_value('msg')
    msg, markup = await ItemService(message.from_user.id, state).give.change_quantity(message.text)
    msg2 = await message.answer(msg, reply_markup=markup)
    await fsm.update_data(msg=msg2)
    await fsm.set_state()
    await msg0.delete()

@admin_router.callback_query(GiveItemActionCall.filter(F.to_give == True))     
@log.decor(arg=True)
@call_exept()
async def callback_handler(callback: CallbackQuery, callback_data: GiveItemCall, state: FSMContext, **kwargs):
    msg = await ItemService(callback.from_user.id, state).give.to_give()
    await callback.message.edit_text(msg)



