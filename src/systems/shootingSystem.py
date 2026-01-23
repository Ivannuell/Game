import math

from systems.system import System

from components.components import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

"""
    1. Checks all entities that can Shoot (ShootIntent) and have a Cannon for shooting (Cannon)
    2. Now iterates through those shooters:
        2.1 - Checks if shooter have fired a shot
        2.2 - gets the shooter's Information for firing
        2.3 - Sets the correct bullet for shooter
        2.4 - Appended the cannon's timer with delta time
        2.5 - Spawned the bullet using the shooters information
        2.5 - Consumed the Shooting intent and reset the cannon's cooldown
"""


class ShootingSystem(System):
    def __init__(self, scene: 'PlayScene'):
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        shooters: 'list[Entity]' = []

        for entity in entities:
            if entity.has(ShootIntent, Cannon):
                shooters.append(entity)

        for shooter in shooters:
            shoot_intent = shooter.get(ShootIntent)

            if not shoot_intent.fired:
                continue

            pos = shooter.get(Position)
            angle = shooter.get(Rotation).angle
            faction = shooter.get(FactionIdentity).faction
            cannon = shooter.get(Cannon)

            speed = 900
            damage = 10
            cannon.time_left += dt

            if faction == "PLAYER":
                damage = 50
            elif faction == "ENEMY":
                damage = 10

            if cannon.cooldown():
                self.scene.proj_pool.spawn(
                    x=pos.x,
                    y=pos.y,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    faction=faction,
                    damage=damage,
                    max_range=1200
                )
                cannon.time_left = 0

            shoot_intent.fired = False
