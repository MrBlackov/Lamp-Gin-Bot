from app.logic.actions.base import (ActionTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    ActionBase,
                                    get_item_for_action_tag)
from app.exeption.action import HaveItemError

class EatAction(ActionBase):
    tag = ActionTags.eat
    is_have_items = True

    name = 'Сьесть'
    emodzi = '🍴'
    description = 'Сьесть предмет.'
    action_text = 'ест'

    commands_text = ['сьесть', 'поесть', 'eat']

    async def to_action(self):
        items = await get_item_for_action_tag(action_tag=self.tag, inventory_id=self.char.exist.inventory.id)
        if items == None or len(items) < 1:
            raise HaveItemError(f'This char(id={self.char.id}) havent item for action')
        return self