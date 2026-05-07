from app.enum_type.tags import ActionTags, SkillTags
from datetime import datetime, timedelta
from app.db.metods.gets import ActionStateDB, CharacterDB, ItemDB, ItemSketchDB, get_item_sketch, get_item_sketch_for_tag, get_exists_for_ids, get_action_state_for_tag, get_action_states_for_block_freedom, get_action_state_for_id, get_action_states_for_exist_id, SkillDB
from app.db.metods.updates import update_skill_for_id, update_skill_for_tag, update_action_state_for_id, update_action_state_for_tag
from app.db.metods.adds import add_db_obj
from app.db.metods.unique import get_chars_for_exist_id, get_item_for_tag, get_item_sketch_for_action_tag, get_item_for_action_tag
from app.db.metods.deletes import delete_action_state, delete_action_states
from app.aio.msg.utils import TextHTML
from app.exeption.action import HaveSkillError, EnergyLessZeroError, HaveItemError
from app.logic.item import ItemsLogic, InventaryOverFlowing
from app.logic.utils import action_point, set_to_list, list_to_set

class ActionBase:
    tag: str | None = None
    default_start = datetime.now
    default_end = None
    default_minute: int | None = None
    default_reset: int = 1
    default_nbt: dict = {}
    default_level: int = 1
    is_block_freedom: bool = False
    is_have_items: bool = False
    spending_time: int | float = 0
    result_item: str | None = None

    name: str = None
    emodzi: str = None
    description: str = None
    action_text: str = None
    to_action_text: str = None
    stop_text: str = 'Остановить'
    stop_emodzi: str = '❌'
    stop = stop_emodzi + ' ' + stop_text

    msg: str = ''
    msg_kwargs: dict = {}
    result = None
    results = None
    to_cmd = True
    to_IKB = True
    commands_text: list[str] = []
    command_prefix: list[str] = ['!', '/']
    IKB = True

    def __init__(self, char: CharacterDB, step: int = 1, minute: int | None = None, action_tags: dict[str, 'ActionBase'] = {}):
        self.char = char
        self.skills = char.exist.attibute_point.skills
        self.energy = char.exist.attibute_point.skill_tags.get(SkillTags.energy)
        self.items = char.exist.inventory.items
        self.step = step
        self.minute = minute if minute else self.default_minute
        self.start = self.default_start() 
        self.end = self.start + timedelta(minutes=self.minute) if self.minute and self.minute > 0 else None
        self.action_tags = action_tags
        self.new_action_state: ActionStateDB | None = None

    @classmethod
    def text(self):
        return f'{self.emodzi} {self.name}'
    
    @classmethod
    def skill_tag(self):
        return self.tag
    
    @classmethod
    def commands(self, to_list: bool = False):
        return [[p,c] for p in self.command_prefix for c in self.commands_text] if to_list else {p:self.commands_text for p in self.command_prefix}

    @property
    def skills_levels_up(self) -> dict[str, int | float] | None:
        return {self.skill_tag(): 0.005} if self.skill_tag() else None

    @property
    def have_skills(self):
        return self.skills_levels_up.keys() if self.skills_levels_up else None

    @classmethod
    def have_items(self):
        return [self.tag] if self.is_have_items else []

    def stats_info(self, **kwargs):
        return []

    async def to_action(self):
        return self
    
    async def dop_action(self):
        return self

    async def get_items(self, action_tag: str) -> list[ItemSketchDB]:
        return await get_item_sketch_for_action_tag(action_tag=action_tag)

    async def to_skill_level_up(self, skill_levels_up: dict[str, int | float] | None):
        if skill_levels_up:
            for skill_tag, level_up in skill_levels_up.items():
                skill = self.char.exist.attibute_point.skill_tags.get(skill_tag)
                skill.level += level_up*skill.sketch.xmod
                skill = await update_skill_for_id(skill.id, new_data={'level':skill.level})
                if skill.sketch.up_level_formula:
                    for tag, xmod in skill.sketch.up_level_formula.items():
                        parent_skill = self.char.exist.attibute_point.skill_tags.get(tag)
                        await update_skill_for_tag(tag=tag, attribute_point_id=self.char.exist.attibute_point.id, new_data={'level':parent_skill.level+level_up*xmod})
            return skill
        
    async def to_state_action(self, action_state: ActionStateDB):
        if self.energy.coins <= 0:
                return await self.to_end(action_state)
        if self.spending_time > 0:
            self.energy.coins -= self.spending_time
            await update_skill_for_id(self.energy.id, {'coins':self.energy.coins})
        now = datetime.now()
        if action_state.end:
            if action_state.end < now:
                return await self.to_end(action_state)
        return await self.state_action(action_state)

    async def to_end(self, action_state: ActionStateDB):
        is_stop = await delete_action_state(id=action_state.id)
        self.result = 'stop' if is_stop else 'is_action'
        self.msg = '{emodzi} {char_name} закончил {name}' if is_stop else '{emodzi} {char_name} продолжает {name}'
        return self
    
    async def state_action(self, action_state: ActionStateDB):
        self.msg = None
        return self

class BlockFreedomAction(ActionBase):
    is_block_freedom: bool = True
    to_action_text = 'начал действие'
    to_cmd = False
    to_IKB = False

    @classmethod
    def stats_info(self, char: CharacterDB, nbt: dict, **kwargs):
        if nbt.get('start_levels'):
            levels_info = []
            for skill_tag, level in nbt['start_levels'].items():
                skill = char.exist.attibute_point.skill_tags.get(skill_tag)
                levels_info.append(f'{skill.sketch.emodzi} {skill.sketch.name}: +{TextHTML.float_format(skill.level-level, 5)} ур.')
            return levels_info
        return []

    async def check(self, have_energy: bool = True, have_skills: bool = True, have_items: bool = True):
        if self.energy.coins <= 0 and have_energy:
            raise EnergyLessZeroError(f'This char(id={self.char.id}) havent energy for action')
        if self.have_skills and have_skills:
            skill_levels = {}
            for skill_tag in self.have_skills:
                skill = self.char.exist.attibute_point.skill_tags.get(skill_tag)
                if skill == None:
                    raise HaveSkillError(f'This char(id={self.char.id}) havent skill for action')
                skill_levels[skill_tag] = skill.level
            self.default_nbt.update({'start_levels':skill_levels})
        if self.have_items() and have_items:
            items = await get_item_for_action_tag(action_tag=self.have_items(), inventory_id=self.char.exist.inventory.id)
            if items == None or len(items) < 1:
                raise HaveItemError(f'This char(id={self.char.id}) havent item for action')
        return True
    
    async def to_action(self):
        await self.check()
        await self.dop_action()
        if self.step == 1:
            self.result = 'to_action_time'
            self.msg = '{emodzi} {char_name} ' + f'[{TextHTML.float_format(self.energy.coins, 7)} ⚡]' + TextHTML('\n'.join([
                f'⏱️ Время до окончания: {self.minute} мин.' if self.minute and self.minute > 0 else '⏱️ Время до окончания: Не ограничено',
                f'⚡ Будет потрачено энергии: {TextHTML.float_format(self.spending_time*self.minute, 7)}' if self.minute and self.minute > 0 else f'⚡ Расход энергии в мин.: {self.spending_time if self.spending_time > 0 else '0'}'
            ])).blockquote()
            return self
        await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.start, end=self.end, nbt=self.default_nbt, exist_id=self.char.exist.id)])
        self.result = 'to_action'
        self.msg = '{emodzi} {char_name} ' + self.to_action_text
        return self

    async def state_action(self, action_state: ActionStateDB):
        self.msg = None
        await self.to_skill_level_up(self.skills_levels_up)
        return self
    
    async def give_item(self, item: ItemDB):
        
        try:
            return await ItemsLogic().give(item.sketch_id, self.char.exist.inventory.id, self.char, item.quantity), True
        except InventaryOverFlowing:
            return await add_db_obj(data=[ItemDB(location_id=1, sketch_id=item.sketch_id, quantity=item.quantity, nbt={"is_pick_up": False})]), False

class StopAction(ActionBase):
    tag = ActionTags.stop

    name = 'Остановиться'
    emodzi = '🧍'
    description = 'Остановиться.'

    to_IKB = False
    commands_text = ['остановиться', 'stop']

    async def to_action(self):
        states = await get_action_states_for_block_freedom(True, self.char.exist.id)
        if states:
            is_stop = await delete_action_states(ids=[s.id for s in states])
            self.result = 'stop'
            self.msg = '{emodzi} {char_name} остановился'
        else:
            self.result = 'no_action'
            self.msg = '❌ {char_name} не занят'
        return self

class StatsAction(ActionBase):
    tag = ActionTags.stats

    to_IKB = False
    commands_text = ['статистика_действия', 'action_stats']

    async def to_action(self):
        states = await get_action_states_for_block_freedom(True, self.char.exist.id)
        state = states[0] if states else None
        if state == None:
            self.IKB = False
            self.msg = f'❌ {self.char.exist.full_name} уже закончил'
            self.result = 'no_action'
            return self
        action = self.action_tags.get(state.tag)
        self.msg = f'{action.emodzi} {self.char.exist.full_name} {action.action_text} '+ f'[{TextHTML.float_format(self.energy.coins, 7)} ⚡]' + TextHTML('\n'.join([
            f'⏱️ Время до окончания: {f'{(state.end - self.default_start()).seconds // 60} мин.' if state.end else "Не ограничено"}',
            f'📉 Расход энергии: {action.spending_time if action.spending_time > 0 else "0"} ⚡'
        ] + action.stats_info(char=self.char, nbt=state.nbt, items=self.items))).blockquote()
        self.result = 'stats'
        return self

class RecoveryAction(ActionBase):
    tag = ActionTags.recovery
    spending_time = -0.1
    to_IKB = False

    name = 'Востановление'
    emodzi = '🛋️'
    description = 'Отдохнуть и восстановить энергию и здоровье.'
    action_text = 'отдыхает'
    to_action_text = 'отдыхает'

    commands_text = ['recovery', 'востановление']

    async def to_action(self):
        state = await get_action_state_for_tag(self.tag, self.char.exist.id)
        if state == None:
            new_state = ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.start, end=None, nbt=self.default_nbt, exist_id=self.char.exist.id)
            state = await add_db_obj(data=[new_state])
        self.msg = f'{self.emodzi} {self.char.exist.full_name} {self.action_text} '+ f'[{str(self.energy.coins)[:7]} ⚡]' + TextHTML('\n'.join([
            f'📈 Восстановление энергии: {-self.spending_time}'
        ])).blockquote()
        self.result = 'recovery'
        return self

    async def to_state_action(self, action_state):
        if self.energy.coins >= self.energy.max_coins:
            return await self.to_end(action_state)
        return await self.state_action(action_state)

    async def to_end(self, action_state):
        return self
    
    async def state_action(self, action_state):
        skill = self.char.exist.attibute_point.skill_tags.get(self.tag)
        self.energy.coins -= self.spending_time*skill.level
        await update_skill_for_id(self.energy.id, {'coins':self.energy.coins})
        return self

    
    


