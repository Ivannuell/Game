

from enum import Enum, auto


class EnemyList(Enum):
    Normal = auto()

class EnemyActions(Enum):
    Patroling = auto()
    Invading = auto()
    Attacking = auto()