from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag)


class RunningAction(BlockFreedomAction):
    tag = ActionTags.running
    is_block_freedom: bool = True
    default_minute = 30
    spending_time = 0.4

    name = 'Бегать'
    emodzi = '🏃'
    description = 'Повышает ловкость и силу.'
    action_text = 'бегает'
    to_action_text = 'начал пробежку'

    to_cmd = True
    to_IKB = True
    commands_text = ['бежать', 'побегaть', 'run']

    @property
    def skills_levels_up(self):
        return {SkillTags.dx: 0.0005}