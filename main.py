import asyncio
from app.aio.config import bot, dp, cmds, admin_cmds, owner, to_menu_cmds
from app.aio.cmd.base import base_router
from app.aio.middlewares.update import UpdateDataMiddleware
from app.aio.middlewares.message_clean import MessageCleanRequestMiddleware
from app.logged.botlog import logs, log, tg_log
from app.exeption import error_faq
from app.scheduler.message import MessageUtils
from app.interlayer.action import ActionLayer
from app.service.drop import DropService

async def loggers():
    return asyncio.create_task(tg_log()) 

async def run_scheduler():
    return await MessageUtils().run_deleter_job()

async def run_state_checker():
    return await ActionLayer(1).state_checker()

async def run_drop_runner():
    return await DropService(1).runner()

async def main():
    c = 1
    try:
        dp.message.middleware(UpdateDataMiddleware())
        bot.session.middleware(MessageCleanRequestMiddleware())
        dp.include_routers(base_router) 
        asyncio.gather(loggers(), run_scheduler(), run_state_checker(), run_drop_runner(), return_exceptions=True)
        log.debug('start polling bot')
        await bot.delete_webhook(drop_pending_updates=True)
        await to_menu_cmds()
        await dp.start_polling(bot)
    except Exception as e:
        logs.critical(f"Polling failed: {e}") 
        if c < 3:
            print(f"⏳ Attempting to restart polling (attempt {c})...")
            await asyncio.sleep(5)  # Подождать перед перезапуском
            c += 1
            await main()
        else:
            raise

if __name__ == "__main__": 
    asyncio.run(main(), debug=True)
    


