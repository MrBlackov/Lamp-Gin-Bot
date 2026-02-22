import asyncio
from app.aio.config import bot, dp, scheduler, cmds, admin_cmds, owner
# from work_time.time_func import send_time_msg
from app.aio.cmd.base import base_router
from app.aio.middlewares.update import UpdateDataMiddleware
from app.logged.botlog import logs, log, tg_log
from app.exeption import error_faq
from app.aio.config import to_menu_cmds

async def loggers():
    return asyncio.create_task(tg_log()) 

async def main():
    try:
        # scheduler.add_job(send_time_msg, 'interval', seconds=10)
        # scheduler.start()
        dp.message.middleware(UpdateDataMiddleware())
        dp.include_routers(base_router) 
        asyncio.gather(loggers(), return_exceptions=True)
        logs.debug('start polling bot')
        await bot.delete_webhook(drop_pending_updates=True)
        await to_menu_cmds()
        await dp.start_polling(bot)
    except Exception as e:
        logs.critical(f"Polling failed: {e}") 

if __name__ == "__main__": 
    asyncio.run(main())
    