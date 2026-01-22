from app.db.dao.base import BaseDAO
from app.db.models.base import TgChatDB, TgUserDB, DonateDB, UserDB

class UserDAO(BaseDAO):
    model = UserDB

class TgChatDAO(BaseDAO):
    model = TgChatDB

class TgUserDAO(BaseDAO):
    model = TgUserDB

class DonateDAO(BaseDAO):
    model = DonateDB
