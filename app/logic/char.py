from app.db.models.char import CharacterDB
from app.validate.info.characters import CharacterInfo, AttributePointsInfo, EXistanceInfo, ItemInfo
from app.logged.botlog import logs
from app.db.models.base import UserDB
from app.db.metods.gets import get_chars_for_user_id, get_char_for_id, get_all_chars, get_main_char_for_user_id, get_user_for_id, get_user_for_tg_id
from app.db.metods.updates import update_main_char
from app.exeption.char import CharError

class CharLogic:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def user_id(self) -> int:
        return await get_user_for_tg_id(self.tg_id)

    async def to_info(self, character: CharacterDB | None = None, char_id: int | None = None):
        if char_id:
            char = await get_char_for_id(char_id)
        elif character:
            char = character
        else:
            raise CharError('This to_info have not char and char_id')
        points = AttributePointsInfo.model_validate(char.exist.attibute_point.__dict__, from_attributes=True)
        exist_dict = char.exist.__dict__
        exist_dict['attibute_point'] = points
        exist_dict['updated_at'] = char.exist.updated_at
        logs.trace(exist_dict)
        exist = EXistanceInfo.model_validate(exist_dict, from_attributes=True)
        char_dict = char.__dict__
        char_dict['exist'] = exist
        new_char = CharacterInfo.model_validate(char_dict, from_attributes=True)
        logs.trace(new_char.model_dump())
        return new_char

    async def get_chars(self, user_id: int) -> list[CharacterInfo] | None:
        chars = []
        char_dbs: list[CharacterDB] = await get_chars_for_user_id(user_id)
        if char_dbs:
            for char_db in char_dbs:
                char = await self.to_info(char_db)
                chars.append(char)
            return chars
        
    async def get_all_chars(self) -> list[CharacterDB]:
        return await get_all_chars()

    async def get_main_char_id(sself, user_id: int) -> int | None:
        return await get_main_char_for_user_id(user_id)

    async def char_to_main(self, user_id: int, char_id: int) -> tuple[list[CharacterInfo], int]:
        new_user: UserDB = await update_main_char(user_id, char_id)
        chars = await self.get_chars(user_id)
        return chars, new_user.main_char




    