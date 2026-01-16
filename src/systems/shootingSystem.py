import math
from typing import TYPE_CHECKING

from entities.bullet import Bullet
from entities.enemy import Enemy
from entities.player import Player
from systems.system import System

from components.components import *


if TYPE_CHECKING:
    from entities.entity import Entity

# class ProjectilePool:
#     def __init__(self, game) -> None:
#         self.game = game
#         self.Proj_Pool: list[Bullet] = [Bullet(self.game) for _ in range(100)]

#     def get(self) -> Bullet | None:
#         for b in self.Proj_Pool:
#             if not b.active:
#                 return b
#         return None


class ShootingSystem(System):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.Projectiles = game.proj_pool

    def update(self, entities: list["Entity"], dt):
        shooters = []

        for entity in entities:
            if entity.has(FireIntent, Cannon):
                shooters.append(entity)

        for shooter in shooters:
            shooter.get(Cannon).time_left += dt

            if shooter.get(FactionIdentity).faction == "PLAYER":
                pos = shooter.get(Position)
                angle = shooter.get(Rotation).rad_angle
                speed = 900
                shooter_faction = shooter.get(FactionIdentity).faction

                if shooter.get(FireIntent).fired:
                    cooldown = shooter.get(Cannon)

                    if cooldown.time_left >= cooldown.cooldown:
                        self.Projectiles.spawn(
                            x=pos.x,
                            y=pos.y,
                            vx=math.cos(angle) * speed,
                            vy=math.sin(angle) * speed,
                            faction=shooter_faction,
                            damage=50,
                            max_range=1200
                        )
                        cooldown.time_left = 0

                shooter.get(FireIntent).fired = False

            elif shooter.get(FactionIdentity).faction == "ENEMY":
                pos = shooter.get(Position)
                angle = shooter.get(Rotation).rad_angle
                speed = 900
                shooter_faction = shooter.get(FactionIdentity).faction

                if shooter.get(FireIntent).fired:
                    cooldown = shooter.get(Cannon)

                    if cooldown.time_left >= cooldown.cooldown:
                        self.Projectiles.spawn(
                            x=pos.x,
                            y=pos.y,
                            vx=math.cos(angle) * speed,
                            vy=math.sin(angle) * speed,
                            faction=shooter_faction,
                            damage=50,
                            max_range=1200
                        )
                        cooldown.time_left = 0

                shooter.get(FireIntent).fired = False
