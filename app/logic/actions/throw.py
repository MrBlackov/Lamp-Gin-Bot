from app.logic.actions.base import (ActionTags, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase)


class ThrowAction(ActionBase):
    tag = ActionTags.throw

    name = 'Кинуть'
    emodzi = '🤾'
    description = 'Кидает предмет.'

    to_cmd = True
    to_IKB = True
    commands_text = ['кинуть', 'throw']

