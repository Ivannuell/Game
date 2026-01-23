
import math
from Utils.helper import ACCELERATION, move_towards
from systems.system import System
from components.components import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene



class MovementSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)
        
    def update(self, entities: 'list[Entity]', dt):
        player_cons = []

        for entity in entities:

            if entity.has(Position, Velocity, MovementIntent):
                player_cons.append(entity)


        for player in player_cons:            
            position = player.get(Position)
            velocity = player.get(Velocity)
            movement_intent = player.get(MovementIntent)
            rotation = player.get(Rotation)

            target_vx = movement_intent.move_x * math.cos(rotation.angle) *  velocity.speed
            target_vy = movement_intent.move_y * -math.sin(rotation.angle) * velocity.speed
        
            if movement_intent.move_x != 0:
                velocity.x = move_towards(velocity.x , target_vx, ACCELERATION * dt)
            # else:
            #     velocity.x = move_towards(velocity.x, 0, FRICTION * dt)

            if movement_intent.move_y != 0:
                velocity.y = move_towards(velocity.y, target_vy, ACCELERATION * dt)
            # else:
            #     velocity.y = move_towards(velocity.y, 0, FRICTION * dt)

            position.x += velocity.x * dt 
            position.y += velocity.y * dt 

    