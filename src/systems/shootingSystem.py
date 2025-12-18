from typing import TYPE_CHECKING

from entities.entity import Entity
from entities.bullet import Bullet
from entities.player import Player

from components.components import Projectile


# if TYPE_CHECKING:

class ShootingSystem:

    def __init__(self, game):
        self.game = game
        self.elapsed_time = 0

    def update(self, entities: list[Entity], dt):
        shooters = []
        
        for entity in entities:
            if entity.has_component('FireIntent') and entity.has_component("Cannon"):
                shooters.append(entity)
      
                
        for shooter in shooters:
            if type(shooter) is Player:
                if shooter.get_component("FireIntent").fired:
                    cooldown = shooter.get_component("Cannon").cooldown

                    if self.elapsed_time >= cooldown:
                        bullet = Bullet(self.game)
                        bullet.add_component(Projectile("Player"))

                        entities.append(bullet)
                        self.elapsed_time = 0

        self.elapsed_time += dt


