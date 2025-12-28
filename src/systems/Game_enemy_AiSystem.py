

import random
from typing import TYPE_CHECKING

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
                move = entity.get(EnemyIntent)
                pos = entity.get(Position)
                movement = entity.get(MovementIntent)

                movement.reset()

                if pos.x < 50:
                    move.move = "RIGHT"
                if pos.x > 500: 
                    move.move = "LEFT"

                if move.move == "LEFT":
                    movement.move_x -= 1
                if move.move == "RIGHT":
                    movement.move_x += 1


class Enemy_AI_ShootingSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.randomPosisitons = [random.randint(100, 1100) for e in range(20)]

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, FireIntent, Position):
                pos = entity.get(Position).x

                if int(pos) in self.randomPosisitons:
                    entity.get(FireIntent).fired = True

                


