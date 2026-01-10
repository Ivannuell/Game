from typing import TYPE_CHECKING
from systems.system import System
from components.components import *

if TYPE_CHECKING:
    from entities.entity import Entity

class HealthSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: list["Entity"], dt):
        for entity in entities:
            if not entity.has(Health):
                continue

            health = entity.get(Health).health
            if health <= 0:
                entity.add(Destroy())



            if not entity.has(Parent):
                continue

            p_health = entity.get(Parent).entity.get(Health)

            if p_health.health <= 0:
                entity.add(Destroy())