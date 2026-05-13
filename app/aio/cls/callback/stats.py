from app.aio.cls.callback.base import BaseCall, MenuCall, BackCall
from typing import Any, Literal

class StatsBackCall(BackCall, prefix='stats_back'):
    pass

class StatsActionCall(BaseCall, prefix='stats_action'):
    to_top: bool = False

class TopActionCall(BaseCall, prefix='top_action'):
    to_skill: bool = False

class TopSkillCall(BaseCall, prefix='top_skill'):
    skill_tag: str








