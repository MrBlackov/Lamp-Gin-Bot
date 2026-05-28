from pydantic import BaseModel, ConfigDict
from app.db.models.item import SkillDB, SkillSketchDB

class CharSketch(BaseModel):
    gender: str
    age: int
    first_name: str
    last_name: str | None
    skills: dict[str, SkillDB]
    products: dict[str, SkillSketchDB]
    all_skills: dict[str, SkillSketchDB]
    coins: int
    user_id: int = 0
    all_first_names: list[str]
    all_last_names: list[str]
    description: str | None = None

    @property
    def no_hide_skills(self):
        return [skill for skill in self.skills.values() if not skill.sketch.is_hide]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


            



