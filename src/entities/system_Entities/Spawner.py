from components.components import *
from entities.entity import Entity

class SpawnerEntity(Entity):
    def __init__(self, pattern, game):
        super().__init__(game)
        self.alive = True
        self.add(SystemEntity())
        self.add(EnemySpawner(pattern))




    