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
            if entity.has(Parent):
                if entity.get(Parent).entity.has(Destroy):
                    entity.add(Destroy())

            if not entity.has(Health):
                continue

            health = entity.get(Health).health
            if health <= 0:
                entity.add(Destroy())


            