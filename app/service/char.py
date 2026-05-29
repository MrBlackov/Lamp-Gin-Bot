from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import AddCharIKB, InfoCharIKB, InventoryIKB, NewCharIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.validate.api.characters import CharSketchInfo
from app.validate.newchar import CharSketch, SkillDB
from app.validate.api.query import CreateCharSkecth
from app.aio.msg.char import SketchInfoText, CharInfoText, InventoryItemsText, NewCharText, CharText
from app.aio.msg.base import UserText
from app.aio.msg.utils import TextHTML
import random
from app.service.base import BaseService 
from app.interlayer.char import CreateCharacterLayer, InfoCharacterLayer, InventoryCharacterLayer, NewCharLayer
from app.aio.cls.fsm.char import InventoryState, NewCharState
from app.exeption.char import BonusCharSubError, NoHaveMainChar, SKillCoinsLessZeroError, SKillLessOneError, SKillLessZeroError
from aiogram.types.chat_member_banned import ChatMemberStatus
from app.exeption.item import ItemError
from app.aio.cls.fsm.utils import CharFSM
from app.logic.query import LetterSearch

class NewCharacterService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.state = CharFSM(state, 'new')
        self.IKB = NewCharIKB(tg_id)
        self.layer = NewCharLayer(tg_id)
        self.text = NewCharText

    async def chouse_gender(self):
        await self.state.clear_this_state()
        my_chars = await InfoCharacterLayer(self.tg_id).get_chars()
        if my_chars.chars:
            if len(my_chars.no_die_chars) == my_chars.max_chars and my_chars.use_bonus == False:
                channel = await self.get_channel_info()
                return '😕 У вас уже максимальное количество персонажей,' \
                ' но вы можете получить бонусного персонажа подписавшись на Газету Нила', self.IKB.get_bonus_char(channel.invite_link)
            if len(my_chars.no_die_chars) > my_chars.max_chars:
                return '😕 У вас уже максимальное количество персонажей', None
        return '📲 Выберите пол', self.IKB.chouse_gender()    

    async def chouse_gender_bonus(self):
        to_member = await self.get_chat_member()
        if to_member:
            if to_member.status != ChatMemberStatus.LEFT and to_member.status != ChatMemberStatus.KICKED:    
                return '📲 Выберите пол', self.IKB.chouse_gender()
        raise BonusCharSubError(f'This user(tg_id:{self.tg_id}) dont sub to newspaper')
    
    async def menu(self, gender: str | None = None):
        await self.state.set_state()
        char_sketch = await self.state.get_value('sketch')
        if char_sketch == None:
            char_sketch = await self.layer.generate_char(gender)
            await self.state.update_data(sketch=char_sketch) 
        return self.text(char_sketch).action_menu(), self.IKB.actions()
    
    async def to_skills(self):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        return f'💡 Навыки [{char_sketch.coins} 💮]', self.IKB.redact_skills(char_sketch.no_hide_skills, 'menu')
    
    async def skills(self, skill_tag: str, level: int, is_base: bool):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        sketch = char_sketch.all_skills.get(skill_tag)
        skill = char_sketch.skills.get(skill_tag)
        if sketch.is_base and level < sketch.min_level:
            raise SKillLessOneError('You can min level of base skill')
        if level < 0:
            raise SKillLessZeroError('You cant less zero level of skill')
        if skill:
            r_level = level - skill.level
            char_sketch.coins -= r_level*sketch.price
        else:
            r_level = 1
            char_sketch.coins -= level*sketch.price
        if char_sketch.coins < 0:
            raise SKillCoinsLessZeroError('You dont have enough skill coins')
        if level > 0:
            skill = SkillDB(level=level, coins=sketch.default_coins, sketch=sketch, sketch_tag=sketch.tag, sketch_id=sketch.id)
            char_sketch.skills[skill_tag] = skill
            if skill_tag in char_sketch.products:
                char_sketch.products.pop(skill_tag)
        else:
            skill = SkillDB(level=level, coins=sketch.default_coins, sketch=sketch, sketch_tag=sketch.tag, sketch_id=sketch.id)
            char_sketch.skills.pop(skill_tag)
            char_sketch.products[skill_tag] = sketch
        await self.state.update_data(sketch=char_sketch)
        return self.text(char_sketch).redact_skill_level(skill), self.IKB.redact_skill_level(skill_tag, level, is_base, 'skills')

    async def to_add_skills(self, values_in_page: int = 10):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        products = list(char_sketch.products.values())
        pages = [tuple(products[i:i+values_in_page]) for i in range(0, len(products), values_in_page)]
        await self.state.update_data(skills_pages=pages, coins=char_sketch.coins)
        return await self.to_page_skills(0)
    
    async def to_page_skills(self, page: int):
        coins = await self.state.get_value('coins')
        pages = await self.state.get_value('skills_pages')
        if pages == None:
            return '💡 Вы добавии все существующие навыки', self.IKB.back('skills')
        return f'💡 Навыки доступные для приобретения [{coins} 💮] {f'[{page + 1}/{len(pages)}стр]' if len(pages) > 1 else ''}', self.IKB.skills(pages[page], page, len(pages), 'skills')
    
    async def to_rename(self, name_type: str | None = None):
        if name_type:
            await self.state.update_data(name_type=name_type)
        else:
            name_type = await self.state.get_value('name_type')
        return f'🔧 Изменение {'имени' if name_type == 'first' else 'фамилии'}', self.IKB.redact_name(name_type, 'menu')

    async def to_random_name(self, name_type: str):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        names: list[str] = char_sketch.all_first_names if name_type == 'first' else char_sketch.all_last_names
        name = random.choice(names)
        return f'🎲 Выпало имя: {name}', self.IKB.random_name(name, name_type, 'rename')
    
    async def to_query_names(self, name_type: str, msg):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        names: list[str] = char_sketch.all_first_names if name_type == 'first' else char_sketch.all_last_names
        print(names)
        await self.state.set_state(NewCharState.part_name)
        await self.state.update_data(name_type=name_type, names=names, msg=msg)
        return f'🔍 Введите часть имени для поиска. \n \n❗ Если имя английское, то часть имени тоже должна быть на английском и т.д.', self.IKB.back('rename')

    async def query_names(self, query_value: str, values_in_page: int = 10):
        names: list[str] = await self.state.get_value('names')
        query_names = LetterSearch(names).search(query_value)
        if len(query_names) > 0:
            pages = [tuple(query_names[i:i+values_in_page]) for i in range(0, len(query_names), values_in_page)]
            await self.state.update_data(names_pages=pages)
            return await self.to_page_names(0)
        else:
            return '❌ Ничего не найдено', self.IKB.back('rename')

    async def to_page_names(self, page: int):
        name_type: str = await self.state.get_value('name_type')
        pages = await self.state.get_value('names_pages')
        return f'📋 Держите список {f'[{page + 1}/{len(pages)}стр]' if len(pages) > 1 else ''}', self.IKB.names(pages[page], name_type, page, len(pages), 'query')

    async def rename(self, name: str | None, name_type: str):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        if name_type == 'first':
            char_sketch.first_name = name
        else:
            char_sketch.last_name = name
        await self.state.update_data(sketch=char_sketch)
        return await self.menu()

    async def to_description(self, msg):
        await self.state.update_data(msg=msg)
        await self.state.set_state(NewCharState.description)
        return '📝 Введите описание персонажа. \n\n❗ Описание может содержать до 1000 символов.', self.IKB.back('menu')

    async def descript(self, description: str):
        char_sketch: CharSketch = await self.state.get_value('sketch')
        char_sketch.description = description
        await self.state.update_data(sketch=char_sketch)
        await self.state.set_state()
        return await self.menu()

    async def create(self, is_finished: bool):
        await self.state.set_state()
        char_sketch: CharSketch = await self.state.get_value('sketch')
        if is_finished or char_sketch.coins == 0:
            await self.layer.add_character(char_sketch)
            await self.state.clear_this_state()
            return '✅ Персонаж успешно создан!', None
        return f'❗ У вас осталось {char_sketch.coins} 💮, они будут конвертированы в фунты.', self.IKB.finish('menu')
        



class AddCharacterService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.state = CharFSM(state, 'add')
        self.IKB = AddCharIKB(tg_id)

    async def chouse_gender(self, to_change: bool = False):
        my_chars = await InfoCharacterLayer(self.tg_id).get_chars()
        if my_chars.chars:
            if len(my_chars.chars) == my_chars.max_chars and my_chars.use_bonus == False:
                channel = await self.get_channel_info()
                return '😕 У вас уже максимальное количество персонажей,' \
                ' но вы можете получить бонусного персонажа подписавшись на Газету Нила', self.IKB.get_bonus_char(channel.invite_link)
            if len(my_chars.chars) > my_chars.max_chars:
                return '😕 У вас уже максимальное количество персонажей', None
        return '📲 Выберите пол', self.IKB.chouse_gender(to_change)
    
    async def chouse_gender_bonus(self, to_change: bool = False):
        to_member = await self.get_chat_member()
        if to_member:
            if to_member.status != ChatMemberStatus.LEFT and to_member.status != ChatMemberStatus.KICKED:    
                return '📲 Выберите пол', self.IKB.chouse_gender(to_change)
        raise BonusCharSubError(f'This user(tg_id:{self.tg_id}) dont sub to newspaper')

    async def to_get_sketchs(self, gender: Gender, to_changes: bool = False):
        if to_changes == False:
            print(gender)
            api_data = await CreateCharacterLayer.get_sketchs(gender)
            logs.debug(f'Class Character give GetSketchs({api_data})')
            await self.state.update_data(
                first_names=api_data.first_names, 
                last_names=api_data.last_names, 
                sketchs=api_data.sketchs, 
                gender=gender,
                free_sketchs_quantity=len(api_data.sketchs)
                )
        return self.IKB.chouse_regim_name()
    
    async def to_sketchs(self, first_names: bool = True):
        names: list[str] = await self.state.get_value('first_names' if first_names else 'last_names')
        sketchs: list = await self.state.get_value('sketchs')
        logs.debug(f'Class Character give GetSketchs({names, sketchs})')
        return self.IKB.chouse_regim_name(first_names)  
    
    async def to_random_name(self, first_names: bool = True):
        datas: list[str] = await self.state.get_value('first_names' if first_names else 'last_names')
        rnd_name = random.choice(datas)
        return self.IKB.get_rnd_name(rnd_name, first_names), rnd_name
    
    async def to_query_names_to_pages(self, query_value: str | None = None, values_in_page: str = 10):
        first_names: bool = await self.state.get_value('is_first_name')
        datas: list[str] = await self.state.get_value('first_names' if first_names else 'last_names', [])
        names = []
        if query_value:
            for data in datas:
                if query_value in data:
                    names.append(data)
        else:
            names = datas
        if len(names) > 0:
            name_pages = [tuple(names[i:i+values_in_page]) for i in range(0, len(names), values_in_page)]
            await self.state.update_data(name_pages=name_pages)
            return self.IKB.get_pages_names(list(name_pages[0]), 0, len(name_pages), first_names), f'📋 Держите список, Страница: 0/{len(name_pages)}'
        else: 
            return self.IKB.query_back(first_names), '❌ Ничего не найдено'
    


    async def get_name_pages(self, page: int):
        first_names: bool = await self.state.get_value('is_first_name')
        pages: list[tuple[str]] = await self.state.get_value('name_pages')
        return self.IKB.get_pages_names(list(pages[page]), page, len(pages), first_names), f'📋 Держите список, Страница: {page}/{len(pages)}'
 
    async def to_chouse_sketchs(self, sketch_id: int = 0, another: bool = False):
        sketchs: list[CharSketchInfo] = await self.state.get_value('sketchs')
        if another:
            sketch_id += 1
        return self.IKB.get_sketchs(sketch_id, len(sketchs)), SketchInfoText(sketchs[sketch_id]).text
     
    async def to_descript(self, sketch_id: int):
        sketchs: list[CharSketchInfo] = await self.state.get_value('sketchs')
        await self.state.update_data(sketch=sketchs[sketch_id])
        return  self.IKB.descript(), 'Описание?'

    async def get_info(self, descript: str | None = None):
        datas: dict = await self.state.get_data()
        first_name = datas.get('first_name')
        last_name = datas.get('last_name')
        sketch = datas.get('sketch')
        description = descript if descript else datas.get('description')

        self.char = CreateCharSkecth(
            first_name=first_name,
            last_name=last_name,
            sketch=sketch,
            description=description
        )
        return self

    @property
    def info_to_str(self):
        text = [f'🪪 {self.char.full_name}', f'\n{SketchInfoText(self.char.sketch).to_text(True)}']
        if self.char.description: text.append(f'\n 📜 Описание \n{TextHTML(TextHTML(self.char.description).blockquote(True)).unescape()}')
        return ''.join(text)
    
    async def markup_to_info(self):
        gender = await self.state.get_value('gender')
        return self.IKB.to_finish(gender)
 
    async def create(self, descript: str | None = None):
        char = await self.get_info(descript)
        user = await CreateCharacterLayer().add_char(self.tg_id, char.char)
        await infolog.new_char(self.tg_id, UserText(user.tg_user, user).text + '\n' + self.info_to_str)
        await self.state.clear_this_state()
        return True

class InfoCharacterService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.state = CharFSM(state, 'info')
        self.IKB = InfoCharIKB(tg_id)
        self.layer = InfoCharacterLayer(self.tg_id)

    async def get_main_char(self):
        char = await self.layer.get_main_char()
        if char == None:
            raise NoHaveMainChar('This user dont choose main char')
        return self.IKB.chouse_main_char(char.id, char.exist.id, True, char.exist.die), CharText(char).text
    
    async def get_chars(self):
        datas = await self.layer.get_chars(None)
        if datas.no_chars:
            return None, '😕 У вас нет персонажей, создать - /newchar'
        chars = {char.id:char for char in datas.chars}
        await self.state.update_data(chars=chars, main_id=datas.main_id)
        return self.IKB.get_list(datas.main_id, chars), '🪪 Ваши персонажи'

    async def get_char(self, char_id: int):
        data: dict = await self.state.get_value('chars')
        main_id: int = await self.state.get_value('main_id')
        if data == None:
            new_data = await self.layer.get_chars(None)
            data = {char.id:char for char in new_data.chars}
        char = await self.layer.get_char(char_id)
        return self.IKB.chouse_main_char(char_id, char.exist.id, (True if char_id == main_id else False), char.exist.die), CharText(char).text
    
    async def char_to_main(self, char_id: int):
        datas = await self.layer.char_to_main(char_id)
        await self.state.update_data(main_id=datas.main_id)
        return await self.get_char(char_id)
    
    async def to_delete_char(self, char_id: int, exist_id: int):
        return self.IKB.to_delete_char(char_id, exist_id), '🙁 Вы точно хотите прервать жизнь персонажа?'

    async def delete_char(self, exist_id: int):
        await self.layer.delete_char(exist_id)
        return await self.get_chars()
    
class InventoryService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.state = CharFSM(state, 'inventory')
        self.IKB = InventoryIKB(tg_id)
        self.text = InventoryItemsText
        self.layer = InventoryCharacterLayer(tg_id)

    async def inventory(self):
        inventory = await self.layer.inventory()
        items = {}
        if inventory.items:
            for item in inventory.items:
                items |= {item.id: item}
            await self.state.update_data(items=items)
            return self.text.inventory(inventory.size/1000, inventory.max_size), self.IKB.items(items)
        return self.text.no_items(), None
        
    async def get_item_info(self, item_id: int):
        items = await self.state.get_value('items')
        skills = await self.layer.all_skills()
        if items == None:
            items = {}
            inventory = await self.layer.inventory()
            if inventory.items:
                for item in inventory.items:
                    items |= {item.id: item}
                await self.state.update_data(items=items)
        await self.state.update_data(item=item_id)
        return self.text.item(items[item_id], skills), self.IKB.action(items[item_id], 'inventory')
        
    async def to_throw(self, msg):
        await self.state.update_data(msg=msg)
        await self.state.set_state(InventoryState.throw_quantity)
        return self.text.throw(), self.IKB.back('item')

    async def throw_away(self, item_id: int, quantity: int):
        throw = await self.layer.throw_away(item_id, quantity)
        if throw: return await self.inventory()
        raise ItemError('Dont throw away')




    async def cmd_pick_up(self, item_id: int | None = None):
        if item_id:
            await self.layer.throw_back(item_id)
        items = await self.layer.look_location_items()    
        await self.state.update_data(location_items=items)
        return await self.location_items()

    async def location_items(self):
        items = await self.state.get_value('location_items') 
        if items: 
            random.shuffle(items)
            return self.text.location_items(), self.IKB.location_items(items[:5], 'location_items', 'inventory')
        return '🕵️ Вокруг нет ничего интересного', None

    async def look_location_item(self, item_id: int):
        item = await self.layer.look_location_item(item_id)
        if item: 
            await self.state.update_data(item_id=item_id)
            return self.text.item(item), self.IKB.pick_up(item.id, 'location_items')
        return '🙁 Уже подобрали', self.IKB.back('location_items', item_id)

    async def to_pick_up(self, item_id: int, msg):
        await self.state.update_data(msg=msg, item_id=item_id)
        await self.state.set_state(InventoryState.pick_up_quantity)
        return self.text.pick_up_quantity(), self.IKB.back('location_item', item_id)
    
    async def pick_up(self, quantity: int):
        item_id = await self.state.get_value('item_id')
        await self.layer.pick_up(item_id, quantity)
        return await self.inventory()
    

class Character:
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        self.tg_id = tg_id
        self.state = state
        self.to_create = AddCharacterService(tg_id, state, message, **kwargs)
        self.new = NewCharacterService(tg_id, state, message, **kwargs)
        self.info = InfoCharacterService(tg_id, state, message, **kwargs)
        self.inventory = InventoryService(tg_id, state, message, **kwargs)
        