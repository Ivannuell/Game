from pygame import Vector2
from components.components import *
from entities.entity import Entity
from registries.EnemyList import EnemyList

class SpawnEvent:
    spawn: EnemyList
    position: Vector2
    direction: float | None = None
    delay: float = 0.0
    target: 'Entity'
    faction: 'str'

class SpawnerEntity(Entity):
    def __init__(self, scene, faction):
        super().__init__(scene)
        self.alive = True
        self.add(UtilityEntity())
        self.add(FactionIdentity(faction))
        self.add(Spawner())



    