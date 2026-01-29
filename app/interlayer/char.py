from app.logic.exist import CreateExistence
from app.logic.dnd import person
from app.validate.service.info import UserChars
from app.enum_type.char import Gender
from app.validate.api.characters import GetSketchsInfo
from app.validate.api.query import CreateCharSkecth
from app.db.metods.gets import get_user_for_tg_id, select_exist, get_main_char_for_user_id, get_char_for_id, get_items_for_inventory
from app.db.metods.updates import update_main_char, update_char, update_exist
from app.db.metods.adds import add_char, add_db_obj
from app.logic.char import CharService
from app.validate.add.characters import Character_add
from app.db.models.char import CharacterDB, ExistenceDB, InventoryDB, AttributePointDB
from app.logic.item import ItemSketchsLogic, ItemsLogic

class CreateCharacter:
    def get_sketchs(gender: Gender = 'M', quantity: int = 5):
        prs = person(gender)
        print(gender)
        sketchs = CreateExistence(gender, prs).create_char_skecths(quantity)
        first_names = prs.names[0]
        last_names = prs.names[1]
        return GetSketchsInfo(sketchs=sketchs, first_names=first_names, last_names=last_names)

    async def add_char(self, tg_id: int, sketch: CreateCharSkecth):
        user_id = await get_user_for_tg_id(tg_id)
        char = CreateExistence(
            gender=sketch.sketch.gender, 
            prs=person(sketch.sketch.gender)
            ).create_char(sketch.full_name, 
                          user_id=user_id, 
                          descript=sketch.description
                          )

        return await self.valid_to_db_model(user_id, char)
    
    async def valid_to_db_model(self, user_id: int, char: Character_add):
        exist = char.exist
        char_db = CharacterDB(user_id=user_id, description=char.description)
        exist_db = ExistenceDB(people_id=char_db.id, 
                                 first_name=exist.first_name, 
                                 last_name=exist.last_name, 
                                 gender=exist.gender,
                                 age=exist.age,
                                 amount_life=exist.amount_life)
        print('1')
        await add_db_obj(data=[char_db, exist_db])
        inventory = exist.inventory
        attibute_point = exist.attibute_point
        inventory_db = InventoryDB(exist_id=exist_db.id)
        attibute_point_db = AttributePointDB(exist_id=exist_db.id, **attibute_point.model_dump())        
        await add_db_obj(data=[inventory_db, attibute_point_db])
        new_exist_db = await select_exist(filters={'id':exist_db.id})
        await update_char(filters={'id':char_db.id}, new_data={'exist':new_exist_db})
        return True

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

    async def locator(self):
        pass

class InventoryCharacter:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def get_char_info(self):
        self.user_id = await get_user_for_tg_id(self.tg_id)
        self.char_id = await get_main_char_for_user_id(self.user_id)
        self.char = await get_char_for_id(self.char_id)
        return self
    
    async def inventory(self):
        self = await self.get_char_info()
        inventory = self.char.exist.inventory
        self.items = await get_items_for_inventory(inventory.id)
        self.max_size = self.char.exist.attibute_point.strength
        size = 0
        for item in self.items:
            size += item.sketch.size*item.quantity
        self.size = size
        return self

    async def throw_away(self, item_id: int, quantity: int = 1):
        return await ItemsLogic().throw_away(item_id, quantity)
