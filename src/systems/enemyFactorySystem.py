
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

from pygame import Vector2

from registries.EnemyList import EnemyList

from components.components import *

from systems.system import System

class SpawnEvent:
    spawn: EnemyList
    position: Vector2
    direction: float | None = None
    delay: float = 0.0
    target: 'Entity'


class Enemy_FactorySystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:

            if not entity.has(EnemySpawner):
                continue

            spawner = entity.get(EnemySpawner)
            pattern = spawner.pattern

            pattern.update_step(dt)

            for event in pattern.get_spawn_events():
                entities.append(self.spawnEnemy(event))

            if pattern.is_done():
                entity.add(Destroy())

                
    def spawnEnemy(self, event: SpawnEvent):
        enemy = self.scene.enemyFactory.create(event.spawn)

        enemy_pos = enemy.get(Position)
        enemy.add(Target(event.target))
        
        enemy_pos.set(event.position)
        enemy.get(Rotation).angle = event.direction

        return enemy