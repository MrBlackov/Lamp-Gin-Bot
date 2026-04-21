from app.aio.cls.callback.base import BaseCall, MenuCall
from typing import Any, Literal

class SkillBackCall(BaseCall, prefix='skill_back'):
    where: str

class SkillPageCall(BaseCall, prefix='skill_page'):
    page: int

class SkillCall(BaseCall, prefix='skill'):
    skill_id: int


    