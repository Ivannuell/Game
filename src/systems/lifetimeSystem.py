from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

from entities.bullet import Bullet
from systems.system import System
from components.components import *

class LifetimeSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)


    def update(self, entities: list['Entity'], dt):
        bullets: list[Bullet] = []
        collided_bullets: list[Bullet] = []

        for entity in entities:
            if entity.has(Projectile):
                bullets.append(entity) #type: ignore

        for entity in entities:
            if not entity.has(CollidedWith):
                continue
            if entity.has(Projectile) and len(entity.get(CollidedWith).entities) > 0:
                collided_bullets.append(entity) #type: ignore
        
        for bullet in collided_bullets:
            others = bullet.get(CollidedWith).entities

            for other in others:
                if bullet.get(FactionIdentity).faction != other.get(FactionIdentity).faction:
                    bullet.active = False 


        for bullet in bullets:
            bullet.get(Projectile).timeout -= dt
            if bullet.get(Projectile).timeout <= 0:
                bullet.active = False 
    
