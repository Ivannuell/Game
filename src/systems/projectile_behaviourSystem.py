
from systems.system import System
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

class ProjectileBehaviourSystem(System):
    elapsed_time = 0

    def update(self, entities: list["Entity"], dt):
        projectiles = []

        for entity in entities:
            if entity.has_component("Projectile"):
                projectiles.append(entity)

