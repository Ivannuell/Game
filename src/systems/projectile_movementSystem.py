
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from systems.system import System

class ProjectileMovementSystem(System):
    def update(self, entities: list["Entity"], dt):
        projectiles = []

        for entity in entities:

            if entity.has_component("Position") and entity.has_component("Projectile"):
                projectiles.append(entity)

        for projectile in projectiles:
            pos = projectile.get_component("Position")
            vel = projectile.get_component("Velocity")
            proj = projectile.get_component("Projectile")

            pos.y -= vel.speed
