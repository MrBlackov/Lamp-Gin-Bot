from app.db.models.char import CharacterDB, ExistenceDB, AttributePointDB, InventoryDB, ItemDB, SkillDB
from app.validate.info.characters import CharacterInfo, AttributePointsInfo, EXistanceInfo, ItemInfo
from app.logged.botlog import logs
from app.db.models.main import UserDB
from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_chars_for_user_id, get_base_skills, get_char_for_id, get_all_chars, get_main_char_for_user_id, get_item_sketch_for_tag, get_user_for_tg_id
from app.db.metods.updates import update_main_char, update_char_die, update_donate_delete_char_quan
from app.exeption.char import CharError
from app.validate.newchar import CharSketch
from app.logic.dnd import CharGenerator, dice, SkillSketchDB

class NewCharLogic:
    async def generate_char(self, gender: str, skills: list[SkillSketchDB], coins: int = 20):
        generator = CharGenerator(gender, coins=coins)
        fn, ln = generator.get_all_names()
        skill_ids = {s.tag:s for s in skills}
        return CharSketch(
            age=generator.to_age(),
            gender=gender,
            first_name=generator.first_name,
            last_name=generator.last_name,
            skills=generator.skills([v for v in skill_ids.values() if v.is_base]),
            products={k:v for k, v in skill_ids.items() if v.is_product},
            all_skills=skill_ids,
            coins=coins,
            all_first_names=fn,
            all_last_names=ln
        )

    def random_generator_char(self, char_sketch: CharSketch):
        return
    
    async def add_char(self, sketch: CharSketch):
        lbs = await get_item_sketch_for_tag('lbs')
        char = await add_db_obj(data=[CharacterDB(user_id=sketch.user_id, description=sketch.description)])
        exist = await add_db_obj(data=[ExistenceDB(people_id=char[0].id, 
                                 first_name=sketch.first_name,
                                 last_name=sketch.last_name,
                                 gender=sketch.gender,
                                 age=sketch.age,
                                 amount_life=sketch.age + 50)])
        inventory = await add_db_obj(data=[InventoryDB(exist_id=exist[0].id)])
        atp = await add_db_obj(data=[AttributePointDB(exist_id=exist[0].id)])
        await add_db_obj(data=[ItemDB(sketch_id=lbs.id, inventory_id=inventory[0].id, quantity = sketch.coins)]) if sketch.coins > 0 else None
        skills = sketch.skills
        all_base_skills = await get_base_skills()
        new_skills = {s.tag:SkillDB(level=s.default_level, coins=s.default_coins, sketch=s, sketch_tag=s.tag, sketch_id=s.id, attribute_point_id=atp[0].id) for s in all_base_skills}
        for skill in skills.values():
            skill.attribute_point_id = atp[0].id
            new_skills[skill.sketch_tag] = skill
        await add_db_obj(data=new_skills.values())
        return char


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

    async def get_chars(self, user_id: int, is_die: bool | None = False) -> list[CharacterInfo] | None:
        chars = []
        char_dbs: list[CharacterDB] = await get_chars_for_user_id(user_id, is_die)
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
    
    async def to_die(self, exist_id: int):
        return await update_char_die(exist_id)




    