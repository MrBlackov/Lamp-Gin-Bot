from aiogram import Router
from app.aio.cmd.char.mychar import char_router
from app.aio.cmd.start import start_router
from app.aio.cmd.faq import faq_router
from app.aio.cmd.transfer import transfer_router

base_router = Router()
base_router.include_routers(start_router, char_router, transfer_router, faq_router)