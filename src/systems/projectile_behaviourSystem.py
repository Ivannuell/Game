
from entities.bullet import Bullet
from systems.system import System
from components.components import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity


class ProjectileBehaviourSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: list["Entity"], dt):
        # projectiles = []

        # for entity in entities:
        #     if entity.has(Projectile):
        #         projectiles.append(entity)

        pass


    
        

