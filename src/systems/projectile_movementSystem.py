
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from systems.system import System
from components.components import *

class ProjectileMovementSystem(System):
    def __init__(self) -> None:
        super().__init__()
    def update(self, entities: list["Entity"], dt):
        projectiles = []

        for entity in entities:

            if entity.has(Position) and entity.has(Projectile):
                projectiles.append(entity)

        for projectile in projectiles:
            pos = projectile.get(Position)
            vel = projectile.get(Velocity)
            proj = projectile.get(Projectile)

            pos.y -= vel.speed
