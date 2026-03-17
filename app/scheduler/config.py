from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.db.base import DATABASE_URL

msg_delete_store = SQLAlchemyJobStore(DATABASE_URL, tablename='message_delete', tableschema='apscheduler')
default_store = SQLAlchemyJobStore(DATABASE_URL, tableschema='apscheduler')
scheduler = AsyncIOScheduler(timezone='UTC')
scheduler.add_jobstore(default_store)
scheduler.add_jobstore(msg_delete_store, 'msg_delete')
