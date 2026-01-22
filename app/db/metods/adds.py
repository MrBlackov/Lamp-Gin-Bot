from app.db.metods.base import add_or_update_obj, add_obj
from app.db.dao.main import TgChatDAO, TgUserDAO
from app.db.dao.chars import CharacterDAO

add_or_update_tg_user = add_or_update_obj(TgUserDAO)
add_or_update_tg_chat = add_or_update_obj(TgChatDAO)

add_char = add_obj(CharacterDAO)
