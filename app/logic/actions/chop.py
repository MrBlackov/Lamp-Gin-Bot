from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags,
                                    add_db_obj,  
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    get_item_sketch,
                                    ItemDB)
import random

class ChopAction(BlockFreedomAction):
    tag = ActionTags.chop
    is_block_freedom: bool = True
    default_minute = 60
    spending_time = 1
    is_have_items = True
    result_item = 'wood'
    default_nbt = {'chop_woods':0, 'damage':0}

    name = 'Рубить деревья'
    emodzi = '🪓'
    description = 'Рубить дерево.'
    action_text = 'рубит дерево'
    to_action_text = 'замахнулся топором'

    to_cmd = True
    to_IKB = True
    commands_text = ['рубить', 'срубить', 'chop']

    @classmethod
    def skill_tag(self):
        return SkillTags.woodcutter

    @property
    def skills_levels_up(self):
        return {self.skill_tag(): 0.0005}

    @classmethod
    def have_items(self):
        return ['axe']

    @classmethod
    def stats_info(self, nbt: dict, **kwargs):
        return super().stats_info(nbt=nbt, **kwargs) + [f'🪓 Добыто древесины: {nbt.get("chop_woods")}🪵']

    async def state_action(self, action_state):
        damage = action_state.nbt.get('damage')
        wood = action_state.nbt.get('wood')
        chop_woods = action_state.nbt.get('chop_woods')
        if wood == None:
            woods = await self.get_items(self.result_item)
            wood = random.choice(woods)
        else:
            wood = await get_item_sketch(wood)
        xp = wood.nbt.get('chop').get('xp') - damage
        skill_tags = self.char.exist.attibute_point.skill_tags
        if xp <= 0:
            quantity = 1
            item, is_have = await self.give_item(ItemDB(inventory_id=self.char.exist.inventory.id, sketch_id=wood.id, quantity=quantity))
            chop_woods += 1 if is_have else 0
            self.msg = f'{self.emodzi} {self.char.exist.full_name} вырубил дерерво {wood.name} ({quantity} шт.)' + (' и положил в свой инвентраь' if is_have else ', и оставил на земле...')
            wood = None
            damage = 0
        else:
            damage += skill_tags.get(SkillTags.st).level*skill_tags.get(SkillTags.woodcutter).level
        action_state.nbt['wood'] = wood.id if wood else None
        action_state.nbt['damage'] = damage        
        action_state.nbt['chop_woods'] = chop_woods
        self.new_action_state = action_state
        await self.to_skill_level_up(self.skills_levels_up)
        return self
   
 
