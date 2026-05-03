from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags, 
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
    is_have_items = True

    name = 'Добывать'
    emodzi = '⛏️'
    description = 'Добывает камень и руду.'
    action_text = 'добывает камень и руду'
    to_action_text = 'замахнулся киркой'

    to_cmd = True
    to_IKB = True
    commands_text = ['добывать', 'mine']

    @property
    def skills_levels_up(self):
        return {SkillTags.miner: 0.0005}