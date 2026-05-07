from app.logic.exist import CreateExistence
from app.logic.dnd import person
from app.validate.service.info import UserChars
from app.enum_type.char import Gender
from app.validate.api.characters import GetSketchsInfo
from app.validate.api.query import CreateCharSkecth
from app.db.metods.gets import get_user_for_tg_id, get_all_skills, get_user_for_id, get_char_for_id, select_exist, get_main_char_for_user_id, get_char_for_id, get_items_for_inventory, get_item_sketchs
from app.db.metods.updates import update_main_char, update_char, update_donate_delete_char_quan, update_char_location_default
from app.db.metods.adds import add_char, add_db_obj
from app.logic.char import CharLogic, NewCharLogic
from app.validate.add.characters import Character_add
from app.db.models.char import CharacterDB, ExistenceDB, InventoryDB, AttributePointDB
from app.logic.item import ItemSketchsLogic, ItemsLogic, ItemDB
from app.logged.infolog import infolog
from app.aio.config import admins, bot, newspaper_id
from aiogram.types.chat_member_banned import ChatMemberStatus
from app.exeption.char import NoHaveMainChar, NoDeleteCharError
from app.exeption.item import PickUpQuantityMoreItemQuantity
from app.interlayer.base import BaseLayer

class NewCharLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = NewCharLogic()

    async def generate_char(self, gender: str):
        skills = await get_all_skills()
        return await self.logic.generate_char(gender, skills)

    async def add_character(self, sketch):
        await self.get_char_info()
        sketch.user_id = self.user.id
        return await self.logic.add_char(sketch)


class CreateCharacterLayer(BaseLayer):
    async def get_sketchs(gender: Gender = 'M', quantity: int = 5):
        prs = person(gender)
        items = await get_item_sketchs()
        sketchs = CreateExistence(gender, prs).create_char_skecths(items, quantity)
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
                          sketch=sketch.sketch,
                          descript=sketch.description
                          )
        

        await self.valid_to_db_model(user_id, char)
        return await get_user_for_tg_id(tg_id, True)  
            
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
        items = [ItemDB(inventory_id=inventory_db.id, sketch_id=item.sketch.id, quantity=item.quantity) for item in inventory.items]       
        await add_db_obj(data=items)
        new_exist_db = await select_exist(filters={'id':exist_db.id})
        await update_char(filters={'id':char_db.id}, new_data={'exist':new_exist_db})
        return True

class InfoCharacterLayer(BaseLayer):
    def __init__(self, tg_id: int):
        self.logic = CharLogic(tg_id)
        self.tg_id = tg_id

    async def get_main_char(self):
        await self.get_char_info()
        return self.char

    async def get_chat_member(self, tg_id: int | None = None):
        if tg_id:
            return await bot.get_chat_member(newspaper_id, tg_id)
        print(newspaper_id)
        return await bot.get_chat_member(newspaper_id, self.tg_id)

    async def get_chars(self, is_die: bool | None = False) -> UserChars:
        self = await self.get_char_info()
        channel_member = await self.get_chat_member()
        use_bonus = False
        if channel_member:
            if channel_member.status != ChatMemberStatus.LEFT and channel_member.status != ChatMemberStatus.KICKED:
                use_bonus = True
        chars = await self.logic.get_chars(self.user.id, is_die)
        if chars:
            main_char_id = await self.logic.get_main_char_id(user_id=self.user.id)
            return UserChars(chars=chars, main_id=main_char_id, max_chars=self.user.donates.char_quantity, use_bonus=use_bonus)
        return UserChars(no_chars=True, max_chars=self.user.donates.char_quantity, use_bonus=use_bonus)

    async def get_char(self, char_id: int):
        return await self.get_char_full_info(char_id)

    async def char_to_main(self, char_id: int):
        user_id = await self.logic.user_id()
        update = await update_main_char(user_id, char_id)
        data = await self.get_chars(None)
        return data

    async def locator(self):
        return await self.logic.get_all_chars()
    
    async def delete_char(self, exist_id: int):
        await self.get_char_info()
        if self.user.donates.delete_char_quantiry == None or self.user.donates.delete_char_quantiry > 0:
            die = await self.logic.to_die(exist_id)
            if die:
                await update_donate_delete_char_quan(self.user.donates.id, self.user.donates.delete_char_quantiry)
                await update_main_char(self.user.id)
                return die
        raise NoDeleteCharError(f'This user(id={self.user.id}) dont have delete_char_quantiry')

class InventoryCharacterLayer(BaseLayer):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.item_logic = ItemsLogic()
    
    async def inventory(self):
        await self.get_char_info()
        if self.char == None:
            raise NoHaveMainChar(f'This user(tg_id:{self.tg_id}) hanst main char')
        inventory = self.char.exist.inventory
        self.items = await get_items_for_inventory(inventory.id)
        self.max_size = self.char.exist.attibute_point.skill_tags.get('inventory').level
        size = 0
        for item in self.items:
            size += item.sketch.size*item.quantity
        self.size = size
        return self

    async def throw_away(self, item_id: int, quantity: int = 1):
        return await self.item_logic.throw_away(item_id, quantity)

    async def look_location_items(self):
        await self.get_char_info()
        await update_char_location_default(self.char_id)
        return await self.item_logic.look_location_items(self.char.exist.location_id, self.char.exist.inventory.id)
    
    async def look_location_item(self, item_id: int):
        await self.get_char_info()
        return await self.item_logic.look_location_item(item_id, self.char.exist.inventory.id)
    
    async def throw_back(self, item_id: int):
        await self.get_char_info()
        return await self.item_logic.throw_back(item_id, self.char.exist.inventory.id)
     
    async def pick_up(self, item_id: int, quantity: int):
        await self.get_char_info()
        item = await self.item_logic.get_item_id(item_id)
        if item.quantity < quantity:
            raise PickUpQuantityMoreItemQuantity(f'This user(user_id:{self.user_id}) enter quantity, but quantity({quantity}) > item.quantity({item.quantity})')
        await self.item_logic.action_for_items([item], self.char, '+', quantity, True)
        return True
        