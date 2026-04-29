from .base import ActionBase, ActionTags, StopAction, WakeUpAction, EatAction, PlayAction, SleepAction, FishingAction, ChopAction, MineAction, ThrowAction, TrainAction, RunningAction, LookAroundAction


actions: list[type[ActionBase]] = [
                                   SleepAction, 
                                   EatAction, 
                                   PlayAction, 
                                   FishingAction, 
                                   ChopAction, 
                                   MineAction, 
                                   ThrowAction, 
                                   TrainAction, 
                                   RunningAction,
                                   LookAroundAction
                                   ]

all_action = actions + [WakeUpAction, StopAction]

action_tags = {a.tag:a for a in all_action}