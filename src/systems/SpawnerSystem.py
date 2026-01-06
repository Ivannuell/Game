
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from pygame import Vector2

from registries.EnemyList import EnemyList

from components.components import Destroy, EnemySpawner, Position, Rotation

from systems.system import System

class SpawnEvent:
    spawn: EnemyList
    position: Vector2
    direction: float | None = None
    delay: float = 0.0


class SpawnerSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:

            if not entity.has(EnemySpawner):
                continue

            spawner = entity.get(EnemySpawner)
            pattern = spawner.pattern

            pattern.update(dt)

            for event in pattern.get_spawn_events():
                entities.append(self.spawnEnemy(event))

            if pattern.is_done():
                entity.add(Destroy)

                


    def spawnEnemy(self, event: SpawnEvent):
        enemy = self.game.spawner.create(event.spawn)

        enemy_pos = enemy.get(Position)
        enemy_pos.set(event.position)

        if event.direction:
            enemy.get(Rotation).rad_angle = event.direction

        return enemy