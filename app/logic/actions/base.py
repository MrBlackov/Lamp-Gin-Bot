from app.enum_type.tags import ActionTags, SkillTags
from datetime import datetime, timedelta
from app.db.metods.gets import ActionStateDB, CharacterDB, get_action_state_for_tag, get_action_states_for_block_freedom, get_skill_sketch_for_tag, get_action_state_for_id, get_action_states_for_exist_id
from app.db.metods.updates import update_skill_sketch_for_tag
from app.db.metods.adds import add_db_obj
from app.db.metods.deletes import delete_action_state, delete_action_states

class ActionBase:
    tag: str = None
    have_start = True
    have_end = False
    default_start = datetime.now
    default_end = None
    default_reset: int = 1
    default_nbt: dict = {}
    default_level: int = 1
    is_block_freedom: bool = False

    name: str = None
    emodzi: str = None
    description: str = None
    action_text: str = None
    to_action_text: str = None
    stop_text: str = 'Остановить'
    stop_emodzi: str = '❌'
    stop = stop_emodzi + ' ' + stop_text

    msg: str = ''
    result = None
    commands_text: list[str] = []
    command_prefix: list[str] = ['!', '/']
    IKB = None

    def __init__(self, char: CharacterDB, step: int):
        self.char = char
        self.step = step

    @classmethod
    def text(self):
        return f'{self.emodzi} {self.name}'
    
    @classmethod
    def commands(self, to_list: bool = False):
        return [[p,c] for p in self.command_prefix for c in self.commands_text] if to_list else {p:self.commands_text for p in self.command_prefix}

    async def to_action(self):
        return self

class BlockFreedomAction(ActionBase):
    is_block_freedom: bool = True
    to_action_text = 'начал действие'

    async def to_action(self):
        await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.default_start(), end=self.default_end, nbt=self.default_nbt, exist_id=self.char.exist.id)])
        self.result = 'to_action'
        self.msg = '{emodzi} {char_name} ' + self.to_action_text
        return self

class StopAction(ActionBase):
    tag = ActionTags.stop

    name = 'Остановиться'
    emodzi = '🧍'
    description = 'Остановиться.'

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

class SleepAction(BlockFreedomAction):
    tag = ActionTags.sleep
    is_block_freedom: bool = True

    name = 'Спать'
    emodzi = '💤'
    description = 'Отдохнуть и восстановить энергию и здоровье.'
    action_text = 'спит'
    to_action_text = 'заснул'
    stop_text = 'Проснуться'
    

    commands_text = ['поспать', 'спать', 'sleep']

    async def to_action(self):
        await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.default_start(), end=self.default_end, nbt=self.default_nbt, exist_id=self.char.exist.id)])
        self.result = 'to_sleep'
        return self

class WakeUpAction(StopAction):
    tag = ActionTags.wake_up

    name = 'Проснуться'
    emodzi = '🌅'
    description = 'Вырваться из сна.'

    commands_text = ['проснуться', 'wake_up']

    async def to_action(self):
        sleep_state = await get_action_state_for_tag('sleep', self.char.exist.id)
        if sleep_state:
            is_wake_up = await delete_action_state(id=sleep_state.id)
            self.result = 'wake_up' if is_wake_up else 'is_sleep'
            self.msg = '{emodzi} {char_name} проснулся' if is_wake_up else '{emodzi} {char_name} спит'
        else:
            self.result = 'no_sleep'
            self.msg = '❌ {char_name} не спит'
        return self
    
class RunningAction(BlockFreedomAction):
    tag = ActionTags.running
    is_block_freedom: bool = True

    name = 'Бегать'
    emodzi = '🏃'
    description = 'Повышает ловкость и силу.'
    action_text = 'бегает'
    to_action_text = 'начал пробежку'

    commands_text = ['бежать', 'побегaть', 'run']
    
class ThrowAction(ActionBase):
    tag = ActionTags.throw

    name = 'Кинуть'
    emodzi = '🤾'
    description = 'Кидает предмет.'

    commands_text = ['кинуть', 'throw']

class FishingAction(BlockFreedomAction):
    tag = ActionTags.fishing
    is_block_freedom: bool = True

    name = 'Рыбачить'
    emodzi = '🎣'
    description = 'Рыбачить.'
    action_text = 'рыбачит'
    to_action_text = 'закинул удочку'

    commands_text = ['рыбачить', 'fishing']

class TrainAction(BlockFreedomAction):
    tag = ActionTags.train
    is_block_freedom: bool = True

    name = 'Тренироваться'
    emodzi = '🏋️'
    description = 'Тренирует силу.'
    action_text = 'тренируется'
    to_action_text = 'начал тренироваться'

    commands_text = ['тренироваться', 'train']

class EatAction(ActionBase):
    tag = ActionTags.eat

    name = 'Сьесть'
    emodzi = '🍴'
    description = 'Сьесть предмет.'
    action_text = 'ест'

    commands_text = ['сьесть', 'поесть', 'eat']

class ChopAction(BlockFreedomAction):
    tag = ActionTags.chop
    is_block_freedom: bool = True

    name = 'Рубить'
    emodzi = '🪓'
    description = 'Рубить дерево.'
    action_text = 'рубит дерево'
    to_action_text = 'замахнулся топором'

    commands_text = ['рубить', 'срубить', 'chop']

class MineAction(BlockFreedomAction):
    tag = ActionTags.mine
    is_block_freedom: bool = True

    name = 'Добывать'
    emodzi = '⛏️'
    description = 'Добывает камень и руду.'
    action_text = 'добывает камень и руду'
    to_action_text = 'замахнулся киркой'

    commands_text = ['добывать', 'mine']

class PlayAction(ActionBase):
    tag = ActionTags.play

    name = 'Играть'
    emodzi = '🎮'
    description = 'Кидает предмет.'
    action_text = 'играет'
    stop_text = 'Прекратить'

    commands_text = ['играть', 'поиграть', 'play']

class LookAroundAction(ActionBase):
    tag = ActionTags.lookaround

    name = 'Осмотреться'
    emodzi = '🕶️'
    description = 'Осмотреть ситуацию вокруг.'
    stop_text = 'Прекратить'

    commands_text = ['осмотреться', 'look']
