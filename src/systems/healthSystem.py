from typing import TYPE_CHECKING
from systems.system import System

if TYPE_CHECKING:
    from entities.entity import Entity

class HealthSystem(System):
    def __init__(self, game):
        self.game = game

    def update(self, entities: list["Entity"], dt):
        for entity in entities:
            if entity.has_component("Health"):
                health = entity.get_component("Health").health
                if health <= 0:
                    entities.remove(entity)    