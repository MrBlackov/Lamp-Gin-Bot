from app.logic.actions.base import (ActionTags, 
                                    ItemDB, 
                                    CharacterDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    TextHTML,
                                    get_char_for_id,
                                    ActionBase,
                                    SettingSelf,
                                    UserDB)
from app.logic.settings import allowed_sender_item
from app.exeption.char import InventaryIsEmpty

class ThrowAction(ActionBase):
    tag = ActionTags.throw

    name = 'Кинуть'
    emodzi = '🥏'
    description = 'Кидает предмет.'

    to_cmd = True
    to_IKB = True
    commands_text = ['кинуть', 'throw']

    def __init__(self, char, user = None, step = 1, minute = None, action_tags = ..., **kwargs):
        super().__init__(char, user, step, minute, action_tags, **kwargs)
        self.quantity: int = kwargs.get('quantity')
        self.purpose_char_id: int = kwargs.get('purpose_char_id')
        self.purpose_char: CharacterDB = kwargs.pop('purpose_char') if kwargs.get('purpose_char') else None
        self.purpose_user: UserDB = kwargs.pop('purpose_user') if kwargs.get('purpose_user') else None

    async def to_action(self):
        if len(self.char.exist.inventory.items) == 0:
            raise InventaryIsEmpty(f'This user dont have items')
        if self.item_id == None and len(self.char.exist.inventory.items) > 0:
            self.result = 'item_throw'
            self.msg = '❔ Какой предмет хотите кинуть?'
            return self
        if self.purpose_char_id == None:
            self.result = 'char_throw'
            self.msg = '❔ Кому хотите кинуть?'
            self.chars = [c for c in await self.get_chars(True) if c.id != self.char.id]
            return self
        item = self.char.exist.inventory.item_ids.get(self.item_id)
        if item == None and len(self.char.exist.inventory.items) > 0:
            self.msg = '❌ Этого предмета у вас нету. Какой предмет хотите кинуть?'
            self.result = 'item_throw'
            return self
        self.logic.item.check_have_item(self.char, item.id, self.quantity)
        parametr: allowed_sender_item = self.purpose_char.parametr_tags.get(allowed_sender_item.tag)
        if self.step == 1:
            self.msg = f'🥏 Кинуть персонажу {self.purpose_char.exist.full_name} {item.to_text(self.quantity)}?'
            self.result = 'throw_menu'
            return self   
        if parametr.value == parametr.redact_values[0] or parametr.value == parametr.redact_values[1] and self.char.user_id in self.purpose_user.friend_ids:
            await self.logic.item.action_for_items([item], self.char, action='-', quantity=self.quantity, is_pick_up=True)  
            await self.give_item(ItemDB(inventory_id=self.purpose_char.exist.inventory.id, sketch_id=item.sketch.id, quantity=self.quantity))
            self.msg = f'🥏 Вы бросили персонажу {self.purpose_char.exist.full_name} {item.to_text(self.quantity)}, и он словил'
            self.purpose_msg = f'🥏 Вы словили {item.to_text(self.quantity)}. Посмотреть - /inventory'
            self.result = 'to_throw'
        else:
            await self.logic.item.throw_away(item=item, quantity=self.quantity)
            self.msg = f'❌ Вы бросили персонажу {self.purpose_char.exist.full_name} {item.to_text(self.quantity)}, но промахнулись...'
            self.result = 'no_throw'   
        return self