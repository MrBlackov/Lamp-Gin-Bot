from app.logic.actions.base import (ActionBase, 
                                    ActionTags,
                                    SkillTags,
                                    add_db_obj,  
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    get_item_sketch,
                                    ItemDB)
import random

class DropAction(ActionBase):
    tag = ActionTags.drop
    default_nbt = {'chop_woods':0, 'damage':0}

    name = 'Проверить дроп'
    emodzi = '🪓'
    description = 'Дроп - это случайные предметы, которые получают группы игроков.'

    to_cmd = True
    to_IKB = True
    commands_text = ['drop']

    async def to_action(self):
        return self
