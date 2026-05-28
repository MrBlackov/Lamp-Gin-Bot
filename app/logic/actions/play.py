from app.logic.actions.base import (ActionTags, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase,
                                    get_item_for_tag)
from app.exeption.action import HaveItemError

class PlayAction(ActionBase):
    tag = ActionTags.play
    is_have_items = True

    name = 'Играть'
    emodzi = '🎮'
    description = 'Кидает предмет.'
    action_text = 'играет'
    stop_text = 'Прекратить'

    commands_text = ['играть', 'поиграть', 'play']

    async def to_action(self):
        items = await get_item_for_tag(tag=self.tag, inventory_id=self.char.exist.inventory.id)
        if items == None or len(items) < 1:
            raise HaveItemError(f'This char(id={self.char.id}) havent item for action')
        return self

