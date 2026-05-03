from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag)


class FishingAction(BlockFreedomAction):
    tag = ActionTags.fishing
    is_block_freedom: bool = True
    spending_time = 0.2
    is_have_items = True

    name = 'Рыбачить'
    emodzi = '🎣'
    description = 'Рыбачить.'
    action_text = 'рыбачит'
    to_action_text = 'закинул удочку'

    to_cmd = True
    to_IKB = True
    commands_text = ['рыбачить', 'fishing']
