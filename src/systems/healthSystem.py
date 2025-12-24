from typing import TYPE_CHECKING
from systems.system import System
from components.components import *

if TYPE_CHECKING:
    from entities.entity import Entity

class HealthSystem(System):
    def update(self, entities: list["Entity"], dt):
        for entity in entities:
            if entity.has(Health):
                health = entity.get(Health).health
                if health <= 0:
                    entities.remove(entity)    