from enum import Enum

class AnimationStateList(Enum):
    IDLE = 0
    MOVE = 1
    IMPACT = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4

class AnimationMode(Enum):
    NORMAL = 0
    LOOP = 1