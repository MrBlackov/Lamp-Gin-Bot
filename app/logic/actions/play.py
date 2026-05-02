from app.logic.actions.base import (ActionTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase)


class PlayAction(ActionBase):
    tag = ActionTags.play

    name = 'Играть'
    emodzi = '🎮'
    description = 'Кидает предмет.'
    action_text = 'играет'
    stop_text = 'Прекратить'

    commands_text = ['играть', 'поиграть', 'play']
