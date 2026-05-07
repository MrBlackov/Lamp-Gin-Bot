from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags, 
                                    ItemSketchDB,
                                    ItemDB,
                                    SkillTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    get_item_for_tag,
                                    get_item_sketch_for_action_tag,
                                    action_point)
import random

class FishingAction(BlockFreedomAction):
    tag = ActionTags.fishing
    is_block_freedom: bool = True
    spending_time = 0.2
    is_have_items = True
    result_item = 'fish'

    name = 'Рыбачить'
    emodzi = '🎣'
    description = 'Рыбачить.'
    action_text = 'рыбачит'
    to_action_text = 'закинул удочку'

    to_cmd = True
    to_IKB = True
    commands_text = ['рыбачить', 'fishing', 'fish']

    @classmethod
    def have_items(self):
        return [self.tag, 'bait']
    
    @property
    def default_nbt(self):
        return {'items':{i.sketch_id:i.quantity for i in self.items if i.sketch.action and self.result_item in i.sketch.action}}

    @classmethod
    def stats_info(self, items: list[ItemDB], nbt: dict, **kwargs):
        inventory_items = {i.sketch_id:i for i in items if i.sketch.action and self.result_item in i.sketch.action}
        nbt_items = nbt.get('items') or {}
        new_items = {i:iq.quantity - nbt_items.get(str(i)) for i, iq in inventory_items.items() if nbt_items.get(str(i))}
        return super().stats_info(nbt=nbt, **kwargs) + [f'🧺 Выловлено: ' + (' '.join([f'{q}{inventory_items.get(i).sketch.emodzi}' for i, q in new_items.items()]) if len(new_items) > 0 else 'Ничего')] 
        
    async def state_action(self, action_state):
        fishs = await self.get_items(self.result_item)
        fish = random.choice(fishs)
        skill_tags = self.char.exist.attibute_point.skill_tags
        points = action_point([random.randint(1, 20), skill_tags.get(SkillTags.luck).level, skill_tags.get(SkillTags.fishing).level])
        if fish.nbt.get('fishing').get('size') <= points:
            quantity = 1
            item, is_have = await self.give_item(ItemDB(inventory_id=self.char.exist.inventory.id, sketch_id=fish.id, quantity=quantity))
            self.msg = f'{self.emodzi} {self.char.exist.full_name} выловил {fish.name} ({quantity} шт.)' + (' и положил в свой инвентраь' if is_have else ', но выронил...')
        await self.to_skill_level_up(self.skills_levels_up)
        return self
    


