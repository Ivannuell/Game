
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from helper import SPRITE_FORWARD_OFFSET
from systems.system import System
from components.components import *

class ProjectileMovementSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.posd: Position

    def update(self, entities: list["Entity"], dt):
        projectiles = []

        for entity in entities:
            if entity.has(Position, Projectile):
                projectiles.append(entity)
                


        for projectile in projectiles:
            pos = projectile.get(Position)
            vel = projectile.get(Velocity) 

            pos.x += vel.x * dt
            pos.y += vel.y * dt
        
