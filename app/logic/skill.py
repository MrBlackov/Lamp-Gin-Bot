from app.db.metods.adds import add_db_obj
from app.db.metods.gets import get_skills_for_attribute_point_id, get_skill_for_sketch_id, get_skill_sketch_for_id, SkillDB, SkillSketchDB

class SkillLogic:
    async def get_my_skills(self, ap_id: int, **kwargs):
        return await get_skills_for_attribute_point_id(ap_id, **kwargs)




