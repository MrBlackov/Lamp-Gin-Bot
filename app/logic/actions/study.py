from app.logic.actions.base import (BlockFreedomAction, 
                                    ActionTags,
                                    SkillTags,
                                    SkillDB, 
                                    StopAction, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    set_to_list,
                                    list_to_set,
                                    get_all_skills)
from app.validate.item import StudyValide
from app.exeption.action import SkillNotStudyError

class StudyAction(BlockFreedomAction):
    tag = ActionTags.study
    is_block_freedom: bool = True
    spending_time = 0.3
    is_have_items = True

    name = 'Изучать'
    emodzi = '🔬'
    description = 'Изучает теорию по навыкам.'
    action_text = 'учит навык'
    to_action_text = 'начал изучать'
    to_cmd = True
    to_IKB = True
    commands_text = ['учиться', 'изучить', 'study']
    
    @property
    def skills_levels_up(self):
        return None
    
    async def dop_action(self):
        book = self.inventory.item_ids.get(self.item_id)
        if self.step != 1:
            study: dict = book.sketch.nbt.get('study')
            study_skills_nbt: list[dict] = study.get('skills')
            skill_tags = self.attibute_point.skill_tags
            for skill_dict in study_skills_nbt:
                study_skill = StudyValide.model_validate(skill_dict)
                if study_skill.level <= skill_tags.get(study_skill.tag, SkillDB(level=0)).level:
                    study_skills_nbt.remove(skill_dict)
            if len(study_skills_nbt) == 0:
                raise SkillNotStudyError('This book_skill dont use')
            study_skill_levels = {ss.get('tag'):(skill_tags.get(ss.get('tag')).level if skill_tags.get(ss.get('tag')) else 0) for ss in study_skills_nbt}
            self.default_nbt.update({'start_levels':study_skill_levels, 'study_skills':study_skills_nbt})
        return await super().dop_action()

    async def state_action(self, action_state):
        study_skills: list[dict] = action_state.nbt.get('study_skills')
        all_skills = {s.tag:s for s in await get_all_skills()}
        skills_up = {}
        new_skills = []
        for skill_dict in study_skills:
            study = StudyValide.model_validate(skill_dict)
            skill = self.attibute_point.skill_tags.get(study.tag)
            if skill:
                if skill.level < study.level:
                    skills_up |= {study.tag:study.up_level}
                else:
                    study_skills.remove(skill_dict)
            else:
                sketch = all_skills.get(study.tag)
                new_skills.append(SkillDB(level=0+study.up_level, coins=sketch.default_coins, sketch=sketch, sketch_tag=sketch.tag, sketch_id=sketch.id, attribute_point_id=self.attibute_point.id))
        self.new_action_state = action_state
        self.new_action_state.nbt['study_skills'] = study_skills
        await self.to_skill_level_up(skills_up)
        await add_db_obj(data=new_skills)
        if len(study_skills) == 0:
            return await self.to_end(self.new_action_state)
        return self
   
 
