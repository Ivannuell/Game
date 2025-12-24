from typing import TYPE_CHECKING

from entities.bullet import Bullet
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

    def update(self, entities: list["Entity"], dt):
        shooters = []
        
        for entity in entities:
            if entity.has(FireIntent) and entity.has(Cannon):
                shooters.append(entity)
      
                
        for shooter in shooters:
            # Should I change this for faction checking?
            if type(shooter) is Player:
                if shooter.get(FireIntent).fired:
                    cooldown = shooter.get(Cannon).cooldown

                    if self.elapsed_time >= cooldown:
                        bullet = Bullet(self.game)
                        bullet.add(Projectile(Player))

                        pos = bullet.get(Position)
                        shooter_pos = shooter.get(Position)
                        shooter_size = shooter.get(Size)

                        pos.x = shooter_pos.x + (shooter_size.width / 2 - bullet.get(Size).width / 2)
                        pos.y = shooter_pos.y + shooter_size.height / 2

                        entities.append(bullet)
                        self.elapsed_time = 0

        self.elapsed_time += dt


