from app.logic.actions.base import (ActionTags,  
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase)


class LookAroundAction(ActionBase):
    tag = ActionTags.lookaround

    name = 'Осмотреться'
    emodzi = '👀'
    description = 'Осмотреть ситуацию вокруг.'
    stop_text = 'Прекратить'

    commands_text = ['осмотреться', 'look']
