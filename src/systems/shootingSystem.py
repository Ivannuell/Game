from entities.entity import Entity
from entities.bullet import Bullet

class ShootingSystem:
    def __init__(self, game):
        self.game = game
        

    def update(self, entities: list[Entity], dt):

        shooters = []
        
        for entity in entities:
            if entity.has_component('FireIntent'):
                shooters.append(entity)
      
                
        for shooter in shooters:
            if shooter.get_component("FireIntent").fired:
                bullet = Bullet(self.game)
                entities.append(bullet)


