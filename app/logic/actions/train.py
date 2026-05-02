from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag)


class TrainAction(BlockFreedomAction):
    tag = ActionTags.train
    is_block_freedom: bool = True
    default_minute = 30
    spending_time = 1

    name = 'Тренироваться'
    emodzi = '🏋️'
    description = 'Тренирует силу.'
    action_text = 'тренируется'
    to_action_text = 'начал тренироваться'

    to_cmd = True
    to_IKB = True
    commands_text = ['тренироваться', 'train']

