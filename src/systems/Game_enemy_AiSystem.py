

from typing import TYPE_CHECKING

from references import ACCELERATION, FRICTION
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
                velocity = entity.get(Velocity)
                movement = entity.get(MovementIntent)

                movement.reset()

                if pos.x < 100:
                    move.move = "RIGHT"
                if pos.x > 1100: 
                    move.move = "LEFT"

                if move.move == "LEFT":
                    movement.move_x -= 1
                if move.move == "RIGHT":
                    movement.move_x += 1

                

                

    @staticmethod
    def move_towards(current, target, max_delta):
        if current < target:
            return min(current + max_delta, target)
        if current > target: 
            return max(current - max_delta, target)
        return target

