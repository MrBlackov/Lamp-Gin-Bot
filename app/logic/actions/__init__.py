from .base import (ActionBase, 
                   ActionTags, 
                   StopAction, 
                   StatsAction,
                   RecoveryAction)
from .chop import ChopAction
from .sleep import SleepAction, WakeUpAction
from .play import PlayAction
from .eat import EatAction
from .fishing import FishingAction
from .mine import MineAction
from .throw import ThrowAction
from .train import TrainAction
from .run import RunningAction
from .look import LookAroundAction
from .items import DiceAction

class ActionSelf:
    all_action: list[type[ActionBase]] = [
                  SleepAction, 
                  PlayAction, 
                  FishingAction, 
                  ChopAction, 
                  MineAction, 
                  ThrowAction, 
                  TrainAction, 
                  RunningAction,
                  LookAroundAction,
                  WakeUpAction, 
                  StopAction, 
                  StatsAction,
                  RecoveryAction,
                  DiceAction
                  ]
    tags = ActionTags

    action_tags = {a.tag:a for a in all_action}
    skill_tags = {a.skill_tag():a for a in all_action if a.skill_tag()}
    cmd_actions = [a for a in all_action if a.to_cmd]
    IKB_actions = [a for a in all_action if a.to_IKB]

    @classmethod
    def item_action(cls) -> dict[str, type[ActionBase]]:
        item_actions = {}
        for a in cls.all_action:
            if a.is_have_items:
                for i in a.have_items():
                    item_actions[i] = a
        return item_actions