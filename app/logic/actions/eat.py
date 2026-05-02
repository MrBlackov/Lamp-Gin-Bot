from app.logic.actions.base import (ActionTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase)


class EatAction(ActionBase):
    tag = ActionTags.eat

    name = 'Сьесть'
    emodzi = '🍴'
    description = 'Сьесть предмет.'
    action_text = 'ест'

    commands_text = ['сьесть', 'поесть', 'eat']

