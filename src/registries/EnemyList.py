

from enum import Enum, auto


class EnemyList(Enum):
    Normal = auto()
    Farmer = auto()

class EnemyActions(Enum):
    Patroling = auto()
    Invading = auto()
    Attacking = auto()