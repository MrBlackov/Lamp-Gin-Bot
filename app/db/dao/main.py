from app.db.dao.base import BaseDAO
from app.db.models.base import TgChatDB, TgUserDB, DonateDB, UserDB, ChatDB, ChatSettingDB, UserSettingDB

class UserDAO(BaseDAO):
    model = UserDB

class TgChatDAO(BaseDAO):
    model = TgChatDB

class TgUserDAO(BaseDAO):
    model = TgUserDB

class DonateDAO(BaseDAO):
    model = DonateDB

class ChatDAO(BaseDAO):
    model = ChatDB

class ChatSettingDAO(BaseDAO):
    model = ChatSettingDB
    
class UserSettingDAO(BaseDAO):
    model = UserSettingDB