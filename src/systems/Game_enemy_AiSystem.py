

import math
import random
from typing import TYPE_CHECKING

from helper import ENEMY_ACCELARATION, move_towards

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
                vel = entity.get(Velocity)

                targetx = math.cos(rotation.rad_angle) * vel.speed
                targety = math.sin(rotation.rad_angle) * vel.speed

                vel.x = move_towards(vel.x, targetx, ENEMY_ACCELARATION)
                vel.y = move_towards(vel.y, targety, ENEMY_ACCELARATION)

                pos.x += vel.x * dt
                pos.y += vel.y * dt


class Enemy_AI_ShootingSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, ShootIntent, Position):
                entity.get(ShootIntent).fired = True

                


