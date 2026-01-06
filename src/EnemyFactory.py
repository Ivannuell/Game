from entities.enemy import Enemy
from registries.EnemyList import EnemyList





class EnemyFactory:
    def __init__(self, game):
        self.game = game

    def create(self, enemy: EnemyList) -> Enemy:   
        
        if enemy == EnemyList.Normal:
            e = Enemy(self.game)
            
            e.game = self.game
            e.init_Entity()

            return e