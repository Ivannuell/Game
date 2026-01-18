from components.components import *
from entities.entity import Entity

class SpawnerEntity(Entity):
    def __init__(self, scene, pattern):
        super().__init__(scene)
        self.alive = True
        self.add(SystemEntity())
        self.add(EnemySpawner(pattern))




    