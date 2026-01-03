from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from systems.system import System
from components.components import *

class LifetimeSystem(System):
    def __init__(self) -> None:
        super().__init__()


    def update(self, entities: list['Entity'], dt):
        bullets: list[Entity] = []
        collided_bullets: list[Entity] = []

        for entity in entities:
            if entity.has(Projectile):
                bullets.append(entity)

        for entity in entities:
            if entity.has(Projectile) and entity.has(CollidedWith):
                collided_bullets.append(entity)


        
        for bullet in bullets:

            timeleft = bullet.get(Projectile)
            timeleft.timeout -= dt
            if timeleft.timeout <= 0:
                entities.remove(bullet)


        for bullet in collided_bullets:
            others = bullet.get(CollidedWith).entities

            for other in others:
                if bullet.get(FactionIdentity).faction != other.get(FactionIdentity).faction:
                    entities.remove(bullet)