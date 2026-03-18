import asyncio
from app.aio.config import bot, dp, cmds, admin_cmds, owner
from app.aio.cmd.base import base_router
from app.aio.middlewares.update import UpdateDataMiddleware
from app.aio.middlewares.message_clean import MessageCleanRequestMiddleware
from app.logged.botlog import logs, log, tg_log
from app.exeption import error_faq
from app.aio.config import to_menu_cmds
from app.scheduler.message import MessageUtils

async def loggers():
    return asyncio.create_task(tg_log()) 

async def run_scheduler():
    return await MessageUtils().run_deleter_job()

async def main():
    try:
        dp.message.middleware(UpdateDataMiddleware())
        bot.session.middleware(MessageCleanRequestMiddleware())
        dp.include_routers(base_router) 
        asyncio.gather(loggers(), return_exceptions=True)
        asyncio.gather(run_scheduler(), return_exceptions=True)
        logs.debug('start polling bot')
        await bot.delete_webhook(drop_pending_updates=True)
        await to_menu_cmds()
        await dp.start_polling(bot)
    except Exception as e:
        asyncio.gather(loggers(), return_exceptions=True)
        asyncio.gather(run_scheduler(), return_exceptions=True)
        logs.critical(f"Polling failed: {e}") 
        return True

if __name__ == "__main__": 
    asyncio.run(main())
    


