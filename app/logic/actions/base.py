from app.enum_type.tags import ActionTags, SkillTags
from datetime import datetime, timedelta
from app.db.metods.gets import ActionStateDB, CharacterDB, get_action_state_for_tag, get_action_states_for_block_freedom, get_skill_sketch_for_tag, get_action_state_for_id, get_action_states_for_exist_id
from app.db.metods.updates import update_skill_for_id, update_action_state_for_id, update_action_state_for_tag
from app.db.metods.adds import add_db_obj
from app.db.metods.deletes import delete_action_state, delete_action_states
from app.aio.msg.utils import TextHTML
from app.exeption.action import SleepCoinsError

class ActionBase:
    tag: str = None
    have_start = True
    have_end = False
    default_start = datetime.now
    default_end = None
    default_minute: int | None = None
    default_reset: int = 1
    default_nbt: dict = {}
    default_level: int = 1
    is_block_freedom: bool = False
    spending_time: int | float = 0

    name: str = None
    emodzi: str = None
    description: str = None
    action_text: str = None
    to_action_text: str = None
    stop_text: str = 'Остановить'
    stop_emodzi: str = '❌'
    stop = stop_emodzi + ' ' + stop_text
    stats_info = []

    msg: str = ''
    msg_kwargs: dict = {}
    result = None
    to_cmd = True
    to_IKB = True
    commands_text: list[str] = []
    command_prefix: list[str] = ['!', '/']
    IKB = True

    def __init__(self, char: CharacterDB, step: int = 1, minute: int | None = None, action_tags: dict[str, 'ActionBase'] = {}):
        self.char = char
        self.skills = char.exist.attibute_point.skills
        self.energy = char.exist.attibute_point.skill_tags.get(SkillTags.energy)
        self.step = step
        self.minute = minute if minute else self.default_minute
        self.start = self.default_start() 
        self.end = self.start + timedelta(minutes=self.minute) if self.minute and self.minute > 0 else None
        self.action_tags = action_tags

    @classmethod
    def text(self):
        return f'{self.emodzi} {self.name}'
    
    @classmethod
    def commands(self, to_list: bool = False):
        return [[p,c] for p in self.command_prefix for c in self.commands_text] if to_list else {p:self.commands_text for p in self.command_prefix}

    async def to_action(self):
        return self
    
    async def to_state_action(self, action_state: ActionStateDB):
        if self.spending_time != 0:
            self.energy.coins -= self.spending_time
            await update_skill_for_id(self.energy.id, {'coins':self.energy.coins})
        now = datetime.now()
        if action_state.end:
            if action_state.end <= now:
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

    async def to_action(self):
        if self.step == 1:
            self.result = 'to_action_time'
            self.msg = '{emodzi} {char_name} ' + f'[{str(self.energy.coins)[:7]} ⚡]' + TextHTML('\n'.join([
                f'⏱️ Время до окончания: {self.minute} мин.' if self.minute else '⏱️ Время до окончания: Не ограничено',
                f'⚡ Будет потрачено энергии: {str(int(self.spending_time*self.minute))[:7]}' if self.minute else f'⚡ Расход энергии: {self.spending_time if self.spending_time > 0 else '0'}'
            ])).blockquote()
            return self
        print(self.minute, self.start, self.end)
        await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.start, end=self.end, nbt=self.default_nbt, exist_id=self.char.exist.id)])
        self.result = 'to_action'
        self.msg = '{emodzi} {char_name} ' + self.to_action_text
        return self

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
        self.msg = f'{action.emodzi} {self.char.exist.full_name} {action.action_text} '+ f'[{str(self.energy.coins)[:7]} ⚡]' + TextHTML('\n'.join([
            f'⏱️ Время до окончания: {f'{(state.end - self.default_start()).seconds // 60} мин.' if state.end else "Не ограничено"}',
            f'📉 Расход энергии: {action.spending_time if action.spending_time > 0 else "0"}'
        ] + action.stats_info)).blockquote()
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
        return await super().to_state_action(action_state)

    async def to_end(self, action_state):
        return self

    
    


