from app.logic.actions.base import (ActionTags,  
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_exists_for_ids,
                                    get_action_states_for_block_freedom,
                                    ActionBase)
import random

class LookAroundAction(ActionBase):
    tag = ActionTags.lookaround

    name = 'Осмотреться'
    emodzi = '👀'
    description = 'Осмотреть ситуацию вокруг.'
    stop_text = 'Прекратить'

    commands_text = ['осмотреться', 'look']

    async def to_action(self):
        states = await get_action_states_for_block_freedom(True)
        print(states)
        exists = await get_exists_for_ids([s.exist_id for s in states])
        exists = {e.id: e for e in exists}
        self.results = [[exists.get(s.exist_id), self.action_tags.get(s.tag)] for s in states]
        print(self.results)
        if len(self.results) > 5:
            self.results = random.sample(self.results, 5)  
        else:
            random.shuffle(self.results)
        self.result = 'lookaround' if len(self.results) > 0 else 'no_lookaround'
        self.msg = '{emodzi} {char_name} видит как' if len(self.results) > 0 else '{emodzi} {char_name} никого не видит'
        return self


