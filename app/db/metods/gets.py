from app.db.metods.base import add_or_update_obj, select_obj, select_objs
from app.db.dao.main import UserDAO, UserDB
from app.db.dao.chars import CharacterDAO, CharacterDB, ExistenceDAO
from app.db.dao.item import ItemDAO, ItemSketchDAO, ItemDB, ItemSketchDB
from app.validate.add.characters import Character_add, Existence_add
from app.validate.add.base import Users_add
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.exeption.char import NoHaveMainChar

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
    if user.main_char:
        return user.main_char
    else:
        raise NoHaveMainChar(f'This user({user_id}) no have main char')

async def get_char_for_id(char_id: int) -> CharacterDB:
    return await select_char(filters={'id':char_id})

async def get_chars_for_user_id(user_id: int) -> list[CharacterDB]:
    return await select_chars(filters={"user_id":user_id})


select_item = select_obj(ItemValide, ItemDAO)
select_items = select_objs(ItemValide, ItemDAO)
select_item_sketch = select_obj(ItemSketchValide, ItemSketchDAO)
select_item_sketchs = select_objs(ItemSketchValide, ItemSketchDAO)

async def get_item(sketch_id: int, inventory_id: int) -> ItemDB:
    return await select_item(filters={'sketch_id':sketch_id, 'inventory_id':inventory_id})

async def get_item_sketch(sketch_id: int) -> ItemSketchDB:
    return await select_item_sketch(filters={'id':sketch_id})

async def get_item_for_id(item_id: int) -> ItemDB:
    return await select_item(filters={'id':item_id})

async def get_item_for_name(name: str) -> ItemDB:
    return await select_item_sketch(filters={'name':name})

async def get_items_for_inventory(inventory_id: int) -> list[ItemDB] | None:
    return await select_items(filters={'inventory_id':inventory_id})

async def get_item_sketchs() -> list[ItemSketchDB]:
    return await select_item_sketchs()
