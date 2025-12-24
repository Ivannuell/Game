from entities.entity import Entity
from systems.system import System
from components.components import *

class CollisionCleanupSystem(System):
    def __init__(self) -> None:
        super().__init__()
    def update(self, entities: list[Entity], dt):
        for e in entities:
            if e.has(CollidedWith):
                e.remove(CollidedWith)
