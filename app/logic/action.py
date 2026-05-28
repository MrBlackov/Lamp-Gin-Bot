from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_skills_for_attribute_point_id, get_skill_for_sketch_id, get_skill_sketch_for_id
from app.logic.actions import ActionSelf, ActionTags, ActionBase

class ActionLogic:
    async def action(self, char, user, tag: str, step: int = 1, minute: int | None = None, **kwargs):
        action = ActionSelf.action_tags.get(tag)
        return await action(char=char, user=user, step=step, minute=minute, action_tags=ActionSelf.action_tags, **kwargs).to_action()

    
 


