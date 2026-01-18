from systems.system import System
from components.components import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

class HealthSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        for entity in entities:
            if entity.has(Parent):
                if entity.get(Parent).entity.has(Destroy):
                    entity.add(Destroy())

            if not entity.has(Health):
                continue

            health = entity.get(Health).health
            if health <= 0:
                entity.add(Destroy())


            