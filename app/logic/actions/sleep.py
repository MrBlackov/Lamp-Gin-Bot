from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    update_skill_for_id)
from app.exeption.action import SleepCoinsError

class SleepAction(BlockFreedomAction):
    tag = ActionTags.sleep
    is_block_freedom: bool = True
    spending_time = -0.6

    name = 'Спать'
    emodzi = '💤'
    description = 'Отдохнуть и восстановить энергию и здоровье.'
    action_text = 'спит'
    to_action_text = 'заснул'
    stop_text = 'Проснуться'

    to_cmd = True
    to_IKB = True
    commands_text = ['поспать', 'спать', 'sleep']

    @classmethod
    def stats_info(self, char, **kwargs):
        skill = char.exist.attibute_point.skill_tags.get(self.tag)
        return [f'📈 Восстановление энергии: {-self.spending_time*skill.level}']

    async def to_action(self):
        if self.energy.coins >= self.energy.max_coins:
            raise SleepCoinsError(f'This char cant sleep, user(id={self.char.user_id}), coins: {self.energy.coins}')
        await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.start, end=self.end, nbt=self.default_nbt, exist_id=self.char.exist.id)])
        self.result = 'to_sleep'
        self.msg = '{emodzi} {char_name} ' + self.to_action_text
        return self

    async def to_state_action(self, action_state):
        if self.energy.coins >= self.energy.max_coins:
            return await self.to_end(action_state)
        return await super().to_state_action(action_state)

    async def to_end(self, action_state):
        is_wake_up = await delete_action_state(id=action_state.id)
        self.result = 'wake_up' if is_wake_up else 'is_sleep'
        self.msg = '{emodzi} {char_name} проснулся' if is_wake_up else '{emodzi} {char_name} спит'
        return self
    
    async def state_action(self, action_state):
        skill = self.char.exist.attibute_point.skill_tags.get(self.tag)
        self.energy.coins -= self.spending_time*skill.level
        await update_skill_for_id(self.energy.id, {'coins':self.energy.coins})
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


