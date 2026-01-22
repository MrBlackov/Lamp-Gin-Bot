from app.logic.exist import CreateExistence
from app.logic.dnd import person
from app.validate.service.info import UserChars
from app.enum_type.char import Gender
from app.validate.api.characters import GetSketchsInfo
from app.validate.api.query import CreateCharSkecth
from app.db.metods.gets import get_user_for_tg_id
from app.db.metods.updates import update_main_char
from app.db.metods.adds import add_char
from app.logic.char import CharService

class CreateCharacter:
    def get_sketchs(gender: Gender = 'M', quantity: int = 5):
        prs = person(gender)
        sketchs = CreateExistence(gender, prs).create_char_skecths(quantity)
        first_names = prs.names[0]
        last_names = prs.names[1]
        return GetSketchsInfo(sketchs=sketchs, first_names=first_names, last_names=last_names)

    async def add_char(tg_id: int, sketch: CreateCharSkecth):
        user_id = await get_user_for_tg_id(tg_id)
        char = CreateExistence(
            gender=sketch.sketch.gender, 
            prs=person(sketch.sketch.gender)
            ).create_char(sketch.full_name, 
                          user_id=user_id, 
                          descript=sketch.description
                          )
        
        await add_char(data=char)

        return char
    
class InfoCharacter:
    async def get_chars(self, tg_id: int) -> UserChars:
        service = CharService(tg_id)
        user_id = await service.user_id()
        chars = await service.get_chars(user_id)
        if chars:
            main_char_id = await service.get_main_char_id(user_id)
            return UserChars(chars=chars, main_id=main_char_id)
        return UserChars(no_chars=True)

    async def char_to_main(self, tg_id: int, char_id: int):
        service = CharService(tg_id)
        user_id = await service.user_id()
        update = await update_main_char(user_id, char_id)
        data = await self.get_chars(tg_id)
        return data

