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

class ActionSelf:
    all_action: list[type[ActionBase]] = [
                  SleepAction, 
                  EatAction, 
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
                  RecoveryAction
                  ]
    tags = ActionTags

    action_tags = {a.tag:a for a in all_action}
    cmd_actions = [a for a in all_action if a.to_cmd]
    IKB_actions = [a for a in all_action if a.to_IKB]



