from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags, 
                                    add_db_obj,  
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag)


class ChopAction(BlockFreedomAction):
    tag = ActionTags.chop
    is_block_freedom: bool = True
    default_minute = 60
    spending_time = 1

    name = 'Рубить'
    emodzi = '🪓'
    description = 'Рубить дерево.'
    action_text = 'рубит дерево'
    to_action_text = 'замахнулся топором'

    to_cmd = True
    to_IKB = True
    commands_text = ['рубить', 'срубить', 'chop']
