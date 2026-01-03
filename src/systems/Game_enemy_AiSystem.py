

import math
import random
from typing import TYPE_CHECKING

from helper import SPRITE_FORWARD_OFFSET

if TYPE_CHECKING:
    from entities.entity import Entity

from components.components import *
from systems.system import System


class Enemy_AI_MovementSystem(System):
    def __init__(self) -> None:
        super().__init__()


    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, MovementIntent, Position, Velocity):
                pos = entity.get(Position)
                rotation = entity.get(Rotation)

                pos.x += math.cos(rotation.rad_angle + SPRITE_FORWARD_OFFSET) * (dt + 1.2)
                pos.y += math.sin(rotation.rad_angle + SPRITE_FORWARD_OFFSET) * (dt + 1.2)

class Enemy_AI_ShootingSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, FireIntent, Position):
                entity.get(FireIntent).fired = True

                


