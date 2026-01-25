from app.db.metods.base import add_or_update_obj, select_obj, select_objs
from app.db.dao.main import UserDAO, UserDB
from app.db.dao.chars import CharacterDAO, CharacterDB, ExistenceDAO
from app.validate.add.characters import Character_add, Existence_add
from app.validate.add.base import Users_add

add_or_update_user = add_or_update_obj(UserDAO)

select_user = select_obj(Users_add, UserDAO)
select_char = select_obj(Character_add, CharacterDAO)
select_chars = select_objs(Character_add, CharacterDAO)
select_exist = select_obj(Existence_add, ExistenceDAO)

async def get_user_for_tg_id(tg_id: int) -> int:
    user = await add_or_update_user(data={'tg_id':tg_id}, tg_id=tg_id)
    return user.id

async def get_user_for_id(user_id: int) -> UserDB:
    return await select_user(filters={'id':user_id})



async def get_main_char_for_user_id(user_id: int) -> int | None:
   user: UserDB = await get_user_for_id(user_id)
   return user.main_char

async def get_char_for_id(char_id: int) -> CharacterDB:
    return await select_char(filters={'id':char_id})

async def get_chars_for_user_id(user_id: int) -> list[CharacterDB]:
    return await select_chars(filters={"user_id":user_id})