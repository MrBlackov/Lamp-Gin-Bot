from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags,
                                    ItemDB, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    set_to_list,
                                    list_to_set,
                                    get_item_sketch)
import random

class MineAction(BlockFreedomAction):
    tag = ActionTags.mine
    is_block_freedom: bool = True
    default_minute = 60 
    spending_time = 1
    is_have_items = True
    result_item = 'mineral'
    default_nbt = {'xpos':0, 'damage':0}

    name = 'Добывать'
    emodzi = '⛏️'
    description = 'Добывает камень и руду.'
    action_text = 'работает в шахте'
    to_action_text = 'замахнулся киркой'

    to_cmd = True
    to_IKB = True
    commands_text = ['добывать', 'mine']

    @property
    def skills_levels_up(self):
        return {SkillTags.miner: 0.0005}
    
    @property
    def have_items(self):
        return ['pickaxe']

    @classmethod
    def stats_info(self, items: list[ItemDB], nbt: dict, **kwargs):
        sheme = nbt.get('sheme')
        xpos = nbt.get('xpos')
        items_ids = {i.sketch_id:i for i in items}
        mine_items = list_to_set(sheme[:xpos])
        minerals = [f'{quan if quan <= items_ids.get(id).quantity else items_ids.get(id).quantity}{items_ids.get(id).sketch.emodzi}' for id, quan in mine_items.items() if items_ids.get(id)]
        results = ['⛏️ Добыто: ' + ' '.join(minerals)] if len(minerals) > 0 else []
        return super().stats_info(nbt=nbt, **kwargs) + results

    async def generate_mine(self, size: int = 100):
        minerals = await self.get_items(self.result_item)
        minerals_sheme = {mineral.id:int(mineral.nbt.get('mine').get('rarity')*size) for mineral in minerals}
        sheme = set_to_list(minerals_sheme)
        random.shuffle(sheme)
        return sheme

    async def dop_action(self):
        sheme = await self.generate_mine()
        self.default_nbt.update({'sheme':sheme})
        return await super().dop_action()

    async def state_action(self, action_state):
        sheme = action_state.nbt.get('sheme')
        xpos = action_state.nbt.get('xpos')
        damage = action_state.nbt.get('damage')
        mine_item = await get_item_sketch(sheme[xpos])
        xp = mine_item.nbt.get('mine').get('xp') - damage
        skill_tags = self.char.exist.attibute_point.skill_tags
        if xp <= 0:
            quantity = 1
            item, is_have = await self.give_item(ItemDB(inventory_id=self.char.exist.inventory.id, sketch_id=mine_item.id, quantity=quantity))
            xpos += 1
            damage = 0
            self.msg = f'{self.emodzi} {self.char.exist.full_name} добыл {mine_item.name} ({quantity} шт.)' + (' и положил в свой инвентраь' if is_have else ', и оставил на земле...')
        else:
            damage += skill_tags.get(SkillTags.st).level*skill_tags.get(SkillTags.miner).level
        action_state.nbt['xpos'] = xpos
        action_state.nbt['damage'] = damage
        self.new_action_state = action_state
        await self.to_skill_level_up(self.skills_levels_up)
        return self
   
 
