import asyncio
from app.aio.config import bot, dp, scheduler
# from work_time.time_func import send_time_msg
from app.aio.cmd import start_router, char_router
from app.aio.middlewares.update import UpdateDataMiddleware
from app.logged.botlog import logs, log, tg_log

async def loggers():
    return asyncio.create_task(tg_log())

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    
    dp.message.middleware(UpdateDataMiddleware())
    dp.include_routers(char_router, start_router) 
    asyncio.gather(loggers(), return_exceptions=True)
    logs.debug('start polling bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    
