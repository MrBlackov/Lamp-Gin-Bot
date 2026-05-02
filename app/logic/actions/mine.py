from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag)


class MineAction(BlockFreedomAction):
    tag = ActionTags.mine
    is_block_freedom: bool = True
    default_minute = 60 
    spending_time = 1

    name = 'Добывать'
    emodzi = '⛏️'
    description = 'Добывает камень и руду.'
    action_text = 'добывает камень и руду'
    to_action_text = 'замахнулся киркой'

    to_cmd = True
    to_IKB = True
    commands_text = ['добывать', 'mine']

