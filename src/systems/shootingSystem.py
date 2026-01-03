import math
from typing import TYPE_CHECKING

from entities.bullet import Bullet
from entities.enemy import Enemy
from entities.player import Player
from helper import SPRITE_FORWARD_OFFSET
from systems.system import System

from components.components import *


if TYPE_CHECKING:
    from entities.entity import Entity

class ShootingSystem(System):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.elapsed_time = 0
        self.last = 0
        self.current = 0

    def update(self, entities: list["Entity"], dt):
        shooters = []
        
        for entity in entities:
            if entity.has(FireIntent, Cannon):
                shooters.append(entity)
      
        for shooter in shooters:
            shooter.get(Cannon).time_left += dt

            if shooter.get(FactionIdentity).faction == "PLAYER":
                if shooter.get(FireIntent).fired:
                    cooldown = shooter.get(Cannon)

                    if cooldown.time_left >= cooldown.cooldown:
                        bullet = Bullet(self.game)
                        bullet.add(Projectile())
                        bullet.add(FactionIdentity("PLAYER"))
                        bullet.add(Rotation())
                        bullet.add(Velocity(900))
                        

                        pos = bullet.get(Position)
                        vel = bullet.get(Velocity)

                        shooter_pos = shooter.get(Position)
                        shooter_size = shooter.get(Size)
                        angle = shooter.get(Rotation).rad_angle + SPRITE_FORWARD_OFFSET

                        pos.x = shooter_pos.x 
                        pos.y = shooter_pos.y

                        bullet.get(Rotation).rad_angle = angle + SPRITE_FORWARD_OFFSET
                        bullet.get(FactionIdentity).owner = shooter

                        vel.x = math.cos(angle) * vel.speed
                        vel.y = math.sin(angle) * vel.speed

                        entities.append(bullet)
                        cooldown.time_left = 0

                shooter.get(FireIntent).fired = False

            if shooter.get(FactionIdentity).faction == "ENEMY":
                if shooter.get(FireIntent).fired:
                    cooldown = shooter.get(Cannon)

                    if cooldown.time_left >= cooldown.cooldown:
                        bullet = Bullet(self.game)
                        bullet.add(Projectile())
                        bullet.add(FactionIdentity("ENEMY"))
                        bullet.add(Rotation())
                        bullet.add(Velocity(900))

                        pos = bullet.get(Position)
                        vel = bullet.get(Velocity)

                        shooter_pos = shooter.get(Position)
                        shooter_size = shooter.get(Size)
                        angle = shooter.get(Rotation).rad_angle + SPRITE_FORWARD_OFFSET

                        pos.x = shooter_pos.x 
                        pos.y = shooter_pos.y

                        bullet.get(Rotation).rad_angle = angle + SPRITE_FORWARD_OFFSET
                        bullet.get(FactionIdentity).owner = shooter

                        vel.x = math.cos(angle) * vel.speed
                        vel.y = math.sin(angle) * vel.speed

                        entities.append(bullet)
                        cooldown.time_left = 0

                # shooter.get(FireIntent).fired = False


