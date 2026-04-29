from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_skills_for_attribute_point_id, get_skill_for_sketch_id, get_skill_sketch_for_id
from app.logic.actions import actions, action_tags, ActionTags, ActionBase, all_action

class ActionLogic:
    async def action(self, char, tag: str, step: int = 1):
        action = action_tags.get(tag)
        return await action(char=char, step=step).to_action()



