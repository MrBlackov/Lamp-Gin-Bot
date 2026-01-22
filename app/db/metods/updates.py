from app.db.metods.base import update_obj
from app.db.dao.main import UserDAO, UserDB

update_user = update_obj(UserDAO)

async def update_main_char(user_id: int, char_id: int) -> bool:
    return await update_user(filters={'id':user_id}, new_data={'main_char':char_id})