from typing import TYPE_CHECKING

from entities.bullet import Bullet
from entities.enemy import Enemy
from entities.player import Player
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

                        pos = bullet.get(Position)
                        shooter_pos = shooter.get(Position)
                        shooter_size = shooter.get(Size)

                        pos.x = shooter_pos.x + (shooter_size.width / 2 - bullet.get(Size).width / 2)
                        pos.y = shooter_pos.y + shooter_size.height / 2

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

                        pos = bullet.get(Position)
                        shooter_pos = shooter.get(Position)
                        shooter_size = shooter.get(Size)

                        pos.x = shooter_pos.x + (shooter_size.width / 2 - bullet.get(Size).width / 2)
                        pos.y = shooter_pos.y + shooter_size.height / 2

                        entities.append(bullet)
                        cooldown.time_left = 0

                shooter.get(FireIntent).fired = False


